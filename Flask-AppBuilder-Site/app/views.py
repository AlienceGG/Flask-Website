#encoding=utf-8
import calendar
from flask import render_template, redirect
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder.widgets import ListThumbnail, ListWidget, ListItem, ListBlock, ShowBlockWidget, ListLinkWidget
from flask.ext.appbuilder.actions import action
from flask.ext.appbuilder.models.group import aggregate_count, aggregate_avg, aggregate_sum
from flask.ext.appbuilder.views import MasterDetailView, ModelView,MasterDetailView0
from flask.ext.appbuilder.baseviews import expose, BaseView
from flask.ext.appbuilder.charts.views import DirectByChartView, GroupByChartView
from flask.ext.babel import lazy_gettext as _

from app import db, appbuilder
from models import ContactGroup, Gender, Contact, CountryStats, Country


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {'contact_group.name': 'Contacts Group'}
    list_columns = ['name', 'personal_celphone', 'birthday', 'contact_group.name']
    list_template = 'contact.html'
    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    add_fieldsets = show_fieldsets

    edit_fieldsets = show_fieldsets

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket", single=False)
    def muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())

class ContactItemModelView(ContactModelView):
    list_title = 'List Contact (Items)'
    list_widget = ListItem
    list_template = 'contact_item.html'

class ContactThumbnailModelView(ContactModelView):
    list_title = 'List Contact (Thumbnails)'
    list_widget = ListThumbnail
    list_template = 'contact_thumbnail.html'

class ContactBlockModelView(ContactModelView):
    list_title = 'List Contact (Blocks)'
    list_widget = ListBlock
    show_widget = ShowBlockWidget
    list_template = 'contact_block.html'

class ContactLinkModelView(ContactModelView):
    list_title = 'List Contact (Links)1111'
    list_widget = ListLinkWidget
    list_template = 'contact_link.html'


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView, ContactItemModelView, ContactThumbnailModelView, ContactBlockModelView, ]
    list_template = 'contact_group.html'
    add_template = 'contact_group_add.html'
    edit_template = 'contact_group_edit.html'
    show_template = 'contact_group_show.html'

class ContactChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)
    chart_title = 'Grouped contacts'
    label_columns = ContactModelView.label_columns
    chart_type = 'PieChart'

    definitions = [
        {
            'group' : 'contact_group.name',
            'series' : [(aggregate_count,'contact_group')]
        },
        {
            'group' : 'gender.name',
            'series' : [(aggregate_count,'contact_group')]
        }
    ]


def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)

def pretty_year(value):
    return str(value.year)


class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = 'Grouped Birth contacts'
    chart_type = 'AreaChart'
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            'group' : 'month_year',
            'formatter': pretty_month_year,
            'series': [(aggregate_count,'contact_group')]
        },
        {
            'group': 'year',
            'formatter': pretty_year,
            'series': [(aggregate_count,'contact_group')]
        }
    ]


class GroupMasterView(MasterDetailView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

#-----------------------------------------------------
#-----------------------------------------------------

def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)

def pretty_year(value):
    return str(value.year)


class CountryStatsModelView(ModelView):
    datamodel = SQLAInterface(CountryStats)
    list_columns = ['temperature', 'power','electricity', 'voltage', 'pressure']
    base_permissions = ['can_list', 'can_show']
    list_title = 'Data show'


class CountryDirectChartView(DirectByChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = 'Direct Data Chart Example'

    definitions = [
        {
            #'label': 'Monthly',
            'group': 'temperature',
            'series': ['power','voltage']
        }
    ]
	
class MasterGroupByChartView(MasterDetailView):
    datamodel = SQLAInterface(Country)
    base_order = ('name','asc')
    related_views = [CountryDirectChartView]

class CountryGroupByChartView(MasterDetailView0):
    datamodel = SQLAInterface(Country)
    base_order = ('name','asc')
    related_views = [CountryDirectChartView]


class CountryPieGroupByChartView(GroupByChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = 'Grouped Data Example (Pie)'
    chart_type = 'PieChart'

    definitions = [
        {
            'label': 'Country Stat',
            'group': 'country.name',
            'series': [(aggregate_sum, 'unemployed')
            ]
        }
    ]





appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", label=_('List Groups'),
                category="Contacts", category_icon='fa-envelope', category_label=_('Contacts'))
appbuilder.add_view(GroupMasterView, "Master Detail Groups", icon="fa-folder-open-o",
                label=_("Master Detail Groups"), category="Contacts")
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope",
                label=_('List Contacts'), category="Contacts")

appbuilder.add_view(ContactLinkModelView, "List Links Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_view(ContactItemModelView, "List Item Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_view(ContactBlockModelView, "List Block Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_view(ContactThumbnailModelView, "List Thumb Contacts", icon="fa-envelope", category="Contacts")

appbuilder.add_separator("Contacts")
appbuilder.add_view(ContactChartView, "Contacts Chart", icon="fa-dashboard",
                label=_('Contacts Chart'), category="Contacts")
appbuilder.add_view(ContactTimeChartView, "Contacts Birth Chart", icon="fa-dashboard",
                label=_('Contacts Birth Chart'), category="Contacts")

appbuilder.add_view(CountryStatsModelView, "Chart Data (Country)", icon="fa-globe",
                label=_('Data Show'), category_icon="fa-dashboard", category="Function Show")
appbuilder.add_view(CountryDirectChartView, "Direct Chart Example", icon="fa-dashboard",
                label=_('Dynamic Monitoring'), category="Function Show")
appbuilder.add_view(MasterGroupByChartView, "Master Chart Example", icon="fa-bar-chart-o",
                label=_('Precision'), category="Function Show")
appbuilder.add_view(CountryGroupByChartView, "Group By Chart Example", icon="fa-bar-chart-o",
                label=_('Mission'), category="Function Show")
appbuilder.add_view(CountryPieGroupByChartView, "Group By Pie Chart Example", icon="fa-bar-chart-o",
                label=_('Model Update'), category="Function Show")
