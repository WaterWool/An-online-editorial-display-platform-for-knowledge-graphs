from django.urls import path

from . import view

urlpatterns = [
    path('InsertPic/', view.InsertPic),
    path('InsertOneNode/', view.InsertOneNode),
    path('InsertOneRel/', view.InsertOneRel),
    path('InsertUser/',view.InsertUser),
    path('InsertRecLay/',view.InsertRecLay),
    path('InsertRecLayByNode/',view.InsertRecLayByNode),
    path('InsertRecLayByDis/',view.InsertRecLayByDis),
    path('InsertRecLayMy/',view.InsertRecLayMy),

    path('SelectPic/', view.SelectPic),
    path('SelectPass/', view.SelectPass),
    path('SelectRecLay/', view.SelectRecLay),
    path('SelectOnePro/',view.SelectOnePro),
    path('SelectOneRel/',view.SelectOneRel),
    path('SelectOneNodeNoRel/',view.SelectOneNodeNoRel),
    path('SelectOneNodeAndRelIn/',view.SelectOneNodeAndRelIn),
    path('SelectOneNodeAndRelOut/',view.SelectOneNodeAndRelOut),
    path('SelectOneNodeByName/', view.SelectOneNodeByName),
    path('SelectTwoNodePath/',view.SelectTwoNodePath),
    path('SelectTwoNodeShortPath/', view.SelectTwoNodeShortPath),
    path('SelectTwoNodeAllShortPath/', view.SelectTwoNodeAllShortPath),
    path('SelectCircuit/', view.SelectCircuit),
    path('SelectDeepNode/',view.SelectDeepNode),
    path('SelectOneTypeAndRel/',view.SelectOneTypeAndRel),
    path('SelectOneTypeNoRel/',view.SelectOneTypeNoRel),
    path('SelectOneClourAndRel/',view.SelectOneClourAndRel),
    path('SelectOneClourNoRel/',view.SelectOneClourNoRel),
    path('SelectRecLayByNode/',view.SelectRecLayByNode),
    path('SelectRecLayByDis/',view.SelectRecLayByDis),

    path('DeletLay/',view.DeleteLay),
    path('DeletePro/',view.DeletePro),
    path('DeleteAllPro/',view.DeleteAllPro),
    path('DeleteOneRel/',view.DeleteOneRel),
    path('DeleteAllRel/',view.DeleteAllRel),
    path('DeleteOneNodeCom/',view.DeleteOneNodeCom),
    path('DeleteOneNodeByName/',view.DeleteOneNodeByName),
    path('DeleteNodeAtt/',view.DeleteNodeAtt),
    path('DeleteNodeLab/',view.DeleteNodeLab),
    path('DeleteOneClourNode/',view.DeleteOneClourNode),
    path('DeleteOneTypeNode/',view.DeleteOneTypeNode),

    path('AddNodeAtt/', view.AddNodeAtt),
    path('AddNodeLab/', view.AddNodeLab),

    path('SetNodeAtt/', view.SetNodeAtt),
    path('SetRelName/', view.SetRelName),

    path('UpdataProByTime/',view.UpdataProByTime),
    path('UpdataLayByTime/',view.UpdataLayByTime),
]