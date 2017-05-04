#include <vtkPacketFileReader.h>
#include <vtkVelodyneHDLSource.h>
#include <vtkVelodyneHDLReader.h>
#include <vtkTimerLog.h>
#include <vtkNew.h>
#include <vtkExecutive.h>
#include <vtkInformation.h>
#include <vtkInformationDoubleVectorKey.h>
#include <vtkStreamingDemandDrivenPipeline.h>
#include <vtkPoints.h>
#include <vtkPointData.h>
#include <vtkDataArray.h>

#include <string>
#include <cstdio>
#include <unistd.h>
#include <math.h>

using namespace std;

int main(int argc, char* argv[])
{
  //std::string calibration(argv[1]);

  double velo_target_fps = 30.0;
  unsigned int sleep_time = round(1000000/velo_target_fps);
  vtkNew<vtkVelodyneHDLSource> velo_source;
  //source->SetCorrectionsFile(calibration);
  velo_source->Update();
  vtkPolyData* velo_vtk_data = velo_source->GetOutput();

  velo_source->Start();

  while (true) {
    velo_source->Poll();
    velo_source->UpdateInformation();

    vtkStreamingDemandDrivenPipeline* e = (vtkStreamingDemandDrivenPipeline*)velo_source->GetExecutive();
    vtkInformation* inf = e->GetOutputInformation(0);
    int numTimeSteps = e->TIME_STEPS()->Length(inf);
    if (numTimeSteps == 0) {
      usleep(sleep_time);
      continue;
    }

    int lastTimeStep = e->TIME_STEPS()->Get(inf, numTimeSteps-1);
    e->SetUpdateTimeStep(0, lastTimeStep);

    velo_source->Update();
    velo_vtk_data = velo_source->GetOutput();
    if (velo_vtk_data->GetNumberOfPoints() > 0) {
      vtkDataArray* intensity = velo_vtk_data->GetPointData()->GetArray(0);
      vtkDataArray* laser_id = velo_vtk_data->GetPointData()->GetArray(1);
      vtkDataArray* azimuth = velo_vtk_data->GetPointData()->GetArray(2);
      vtkDataArray* distance_m = velo_vtk_data->GetPointData()->GetArray(3);
      vtkDataArray* timestamp = velo_vtk_data->GetPointData()->GetArray(4);
      vtkDataArray* pointcloud = velo_vtk_data->GetPoints()->GetData();
      cout << velo_vtk_data->GetNumberOfPoints() << endl;
      // If you have PCL, you can convert between VTK & PCL using convertToPCL and convertToVTK in VTKUtils
    }

    usleep(sleep_time);
  }

  return 0;
}
