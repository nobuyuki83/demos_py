import moderngl
from PyQt5 import QtWidgets
import numpy

from pathlib import Path

from util_moderngl_qt.drawer_meshpos import DrawerMesPos, ElementInfo
import util_moderngl_qt.qtglwidget_viewer3
import del_msh

if __name__ == "__main__":

    newpath = Path('.') / 'asset' / 'HorseSwap.obj'
    vtx_xyz, elem_vtx_index, elem_vtx_xyz = del_msh.load_wavefront_obj(str(newpath))
    vtx_xyz[:,0] -= (vtx_xyz[:,0].max()+vtx_xyz[:,0].min())*0.5
    vtx_xyz[:,1] -= (vtx_xyz[:,1].max()+vtx_xyz[:,1].min())*0.5
    vtx_xyz[:,2] -= (vtx_xyz[:,2].max()+vtx_xyz[:,2].min())*0.5
    elem_vtx_xyz = elem_vtx_xyz.astype(numpy.uint64)

    E = del_msh.edges_of_triquad_mesh(elem_vtx_index, elem_vtx_xyz, vtx_xyz.shape[0])
    T = del_msh.triangles_from_triquad_mesh(elem_vtx_index, elem_vtx_xyz)

    with QtWidgets.QApplication([]) as app:
        drawer = DrawerMesPos(
            V=vtx_xyz.astype(numpy.float32),
            element=[
                ElementInfo(index=E.astype(numpy.uint32), color=(0, 0, 0), mode=moderngl.LINES),
                ElementInfo(index=T.astype(numpy.uint32), color=(1, 1, 1), mode=moderngl.TRIANGLES)]
        )
        win = util_moderngl_qt.qtglwidget_viewer3.QtGLWidget_Viewer3([drawer])
        win.show()
        app.exec()




