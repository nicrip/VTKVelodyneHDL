import vtk
import vtkVelodyneHDLPython as vv
from vtk.util import numpy_support as nps
import time, threading, datetime

def startVelo():
    global velo_vtk_data

    velo_target_fps = 30.0
    velo_source = vv.vtkVelodyneHDLSource()
    velo_source.Update()
    velo_vtk_data = velo_source.GetOutput()

    def updateVeloSource():
        while True:
            velo_source.Poll()
            velo_source.UpdateInformation()

            e = velo_source.GetExecutive()
            inf = e.GetOutputInformation().GetInformationObject(0)
            numTimeSteps = e.TIME_STEPS().Length(inf)
            if not numTimeSteps:
                time.sleep(1.0/velo_target_fps)
                continue

            lastTimeStep = e.TIME_STEPS().Get(inf, numTimeSteps-1)
            e.SetUpdateTimeStep(0, lastTimeStep)

            velo_source.Update()
            velo_vtk_data = velo_source.GetOutput()
            time.sleep(1.0/velo_target_fps)

    updateThread = threading.Thread(target=updateVeloSource)
    updateThread.daemon = True
    updateThread.start()
    velo_source.Start()

startVelo() #starts a thread that continuously receives Velodyne data

# process the data as you see fit (we assume that processing takes longer than acquisition)
while True:
    if velo_vtk_data.GetNumberOfPoints() > 0:
        intensity = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(0))
        laser_id = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(1))
        azimuth = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(2))
        distance_m = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(3))
        timestamp = nps.vtk_to_numpy(velo_vtk_data.GetPointData().GetArray(4))
        pointcloud = nps.vtk_to_numpy(velo_vtk_data.GetPoints().GetData())
        print pointcloud
        time.sleep(1)