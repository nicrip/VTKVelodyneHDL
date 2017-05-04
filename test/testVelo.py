import vtk
import vtkVelodyneHDLPython as vv
from vtk.util import numpy_support as nps
import time, threading, datetime

def startVelo():
    velo_target_fps = 30.0
    velo_source = vv.vtkVelodyneHDLSource()
    #velo_source.SetCorrectionsFile('/path/to/calibration/file.xml')
    velo_source.Update()
    velo_vtk_data = velo_source.GetOutput()

    velo_source.Start()

    while True:
        velo_source.Poll()
        velo_source.UpdateInformation()

        e = velo_source.GetExecutive()
        inf = e.GetOutputInformation(0)
        numTimeSteps = e.TIME_STEPS().Length(inf)
        if not numTimeSteps:
            time.sleep(1.0/velo_target_fps)
            continue

        lastTimeStep = e.TIME_STEPS().Get(inf, numTimeSteps-1)
        e.SetUpdateTimeStep(0, lastTimeStep)

        velo_source.Update()
        velo_vtk_data = velo_source.GetOutput()
        if velo_vtk_data.GetNumberOfPoints() > 0:
            intensity = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(0))
            laser_id = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(1))
            azimuth = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(2))
            distance_m = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(3))
            timestamp = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(4))
            pointcloud = nps.vtk_to_numpy(velo_vtk_data.GetPoints().GetData())
            print pointcloud
        time.sleep(1.0/velo_target_fps)

startVelo()
