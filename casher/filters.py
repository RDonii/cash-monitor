from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter, DateFromToRangeFilter
from casher.models import Action


class ActionRangeFilter(FilterSet):
    # type = ModelChoiceFilter(field_name='employee__organization', queryset=Organization.objects.all()) # given org's employees only
    date = DateFromToRangeFilter(label='date', field_name='issued')
    # organization = ModelChoiceFilter(field_name='location__organization', queryset=Organization.objects.all())

    class Meta:
        model = Action
        fields= ['category', 'category__type', 'date']