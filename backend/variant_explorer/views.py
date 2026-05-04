from typing import TYPE_CHECKING

from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import filters, pagination, viewsets

from variant_explorer.models import Variant
from variant_explorer.serializers import GeneSerializer, VariantSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest, HttpResponse


PAGE_SIZE = 15


def _filter_variants(search: str) -> "QuerySet":
    """Shared queryset used by both SSR views and the DRF VariantViewSet."""
    qs = Variant.objects.exclude(gene='')
    search = (search or '').strip()
    if search:
        qs = qs.filter(gene__icontains=search)
    return qs


def index_view(request: "HttpRequest") -> "HttpResponse":
    """Full-page shell: search form + initial table render."""
    search = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)

    paginator = Paginator(_filter_variants(search), PAGE_SIZE)
    page = paginator.get_page(page_number)

    return render(request, 'variant_explorer/index.html', {
        'page': page,
        'search': search,
        'page_size': PAGE_SIZE,
    })


def variant_rows_view(request: "HttpRequest") -> "HttpResponse":
    """HTMX partial: returns the table-body + pagination footer fragment."""
    search = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)

    paginator = Paginator(_filter_variants(search), PAGE_SIZE)
    page = paginator.get_page(page_number)

    return render(request, 'variant_explorer/_variant_rows.html', {
        'page': page,
        'search': search,
        'page_size': PAGE_SIZE,
    })


class VariantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows queries to fetch Variant data.
    """
    queryset = Variant.objects.exclude(gene='')
    serializer_class = VariantSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('gene', )


class GeneViewSetPagination(pagination.PageNumberPagination):
    page_size = 100


class GeneViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the gene autosuggest feature
    """
    queryset = Variant.objects.exclude(gene='').values('gene').distinct()
    serializer_class = GeneSerializer
    pagination_class = GeneViewSetPagination

    def get_queryset(self) -> "QuerySet":
        gene_suggest = self.request.query_params.get('geneSuggest', '').strip()
        return self.queryset.filter(gene__contains=gene_suggest.upper()) if gene_suggest else self.queryset
