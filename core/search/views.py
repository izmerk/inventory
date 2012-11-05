from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse

from mozdns.api.v1.api import v1_dns_api
from mozdns.utils import get_zones

import pdb
from core.search.compiler.django_compile import compile_to_django
from core.search.compiler.django_compile import compile_q_objects
from core.search.compiler.invfilter import BadDirective
import simplejson as json
from gettext import gettext as _

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('core.search', 'templates'))

def resource_for_request(resource_name, filters, request):
    resource = v1_dns_api.canonical_resource_for(resource_name)
    objects = resource.get_object_list(request).filter(filters)
    search_fields = resource._meta.object_class.search_fields
    return [(search_fields, resource.model_to_data(model, request)) for model in objects]

def request_to_search(request):
    search = request.GET.get("search", None)
    adv_search = request.GET.get("advanced_search", "")

    if adv_search:
        if search:
            search += " AND " + adv_search
        else:
            search = adv_search
    return search


def handle_shady_search(search):
    if not search:
        return HttpResponse("What do you want?!?")
    dos_terms = ["10", "com", "mozilla.com", "mozilla",  "network:10/8",
            "network:10.0.0.0/8"]
    if search in dos_terms:
        return HttpResponse("Denial of Service attack prevented. The search "
                "term '{0}' is to general".format(search))
    return None

def search_ajax(request):
    template = env.get_template('search/core_search_results.html')
    def html_response(**kwargs):
        return template.render(**kwargs)
    return _search(request, html_response)

def search_dns_text(request):
    template = env.get_template('search/core_search_results.txt')
    def render_rdtype(rdtype_set, **kwargs):
        response_str = ""
        for obj in rdtype_set:
            response_str += _("{0:<6}".format(obj.pk) +
                                obj.bind_render_record(**kwargs) + "\n")
        return response_str
    def text_response(**kwargs):
        response_str = ""
        response_str += render_rdtype(kwargs['soas'])
        response_str += render_rdtype(kwargs['nss'])
        response_str += render_rdtype(kwargs['mxs'])
        response_str += render_rdtype(kwargs['srvs'])
        response_str += render_rdtype(kwargs['cnames'])
        response_str += render_rdtype(kwargs['sshfps'])
        response_str += render_rdtype(kwargs['txts'])
        response_str += render_rdtype(kwargs['addrs'])
        response_str += render_rdtype(kwargs['intrs'])
        response_str += render_rdtype(kwargs['ptrs'])
        response_str += render_rdtype(kwargs['intrs'], reverse=True)
        return response_str

    return _search(request, text_response)

def _search(request, response):
    search = request_to_search(request)

    errors = handle_shady_search(search)
    if errors:
        return errors

    objs, error_resp = compile_to_django(search)
    if not objs:
        return HttpResponse(json.dumps({'error_messages': error_resp}))
    (addrs, cnames, domains, mxs, nss, ptrs, soas, srvs, sshfps, intrs, sys,
            txts, misc) = objs
    meta = {
            'counts':{
                'addr': addrs.count() if addrs else 0,
                'cname': cnames.count() if cnames else 0,
                'domain': domains.count() if domains else 0,
                'intr': intrs.count() if intrs else 0,
                'sys': sys.count() if sys else 0,
                'mx': mxs.count() if mxs else 0,
                'ns': nss.count() if nss else 0,
                'soa': soas.count() if soas else 0,
                'ptr': ptrs.count() if ptrs else 0,
                'txt': txts.count() if txts else 0,
                }
            }
    return HttpResponse(response(
                                    **{
                                        "misc": misc,
                                        "addrs": addrs,
                                        "cnames": cnames,
                                        "domains": domains,
                                        "intrs": intrs,
                                        "sys": sys,
                                        "mxs": mxs,
                                        "nss": nss,
                                        "ptrs": ptrs,
                                        "soas": soas,
                                        "sshfps": sshfps,
                                        "srvs": srvs,
                                        "txts": txts,
                                        "meta": meta,
                                        "search": search
                                    }
                        ))
def search(request):
    """Search page"""
    search = request.GET.get('search','')
    return render(request, "search/core_search.html", {
        "search": search,
        "zones": [z.name for z in get_zones()]
    })

def get_zones_json(request):
    return HttpResponse(json.dumps([z.name for z in get_zones()]))
