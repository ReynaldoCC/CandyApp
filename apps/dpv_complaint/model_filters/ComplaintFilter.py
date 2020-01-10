from apps.dpv_complaint.models import Complaint
import django_filters


class ComplaintFilter(django_filters.FilterSet):
    class Meta:
        model = Complaint
        fields = ['body', 'topic', 'status', 'origin', 'enter_date']
