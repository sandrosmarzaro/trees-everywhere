from django.urls import path

from . import views

app_name = 'trees'

urlpatterns = [
    path(
        'trees/',
        views.TreeListCreateAPIView.as_view(),
        name='tree-list-create',
    ),
    path(
        'trees/<uuid:pk>/',
        views.TreeRetrieveUpdateDestroyAPIView.as_view(),
        name='tree-detail',
    ),
    path(
        'trees-planted',
        views.PlantedTreeCreateAPIView.as_view(),
        name='planted-tree-create',
    ),
    path(
        'trees-planted/my/',
        views.PlantedTreeListByUserAPIView.as_view(),
        name='planted-tree-list-by-user',
    ),
    path(
        'trees-planted/accounts/',
        views.PlantedTreeListByAccountsAPIView.as_view(),
        name='planted-tree-list-by-accounts',
    ),
    path(
        'trees-planted/bulk/',
        views.PlantedTreeBulkCreateAPIView.as_view(),
        name='planted-tree-bulk-create',
    ),
    path(
        'trees-planted/<uuid:pk>/',
        views.PlantedTreeAPIView.as_view(),
        name='planted-tree-detail',
    ),
]
