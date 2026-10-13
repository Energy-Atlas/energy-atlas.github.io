---
overview: true
---

# Voxel Shading Guide Index

These guides explain the source implementation behind the voxel-shading API surfaces documented in:

- [Python API reference](../../python/index.md)
- [Web API reference](../../web-api/index.md)

## Read Sequence

1. [Voxelization, sensor generation, and shading pipeline](voxelization-sensors-calculation.md)
2. [Sunlit fraction calculation](sunlit-fraction.md)
3. [Sky and horizon view factors](sky-horizon-view-factors.md)
4. [Incident radiation from weather and shading](incident-radiation.md)

## Guide Files

| Guide | Purpose | Main API links |
| --- | --- | --- |
| [Sky and horizon view factors](sky-horizon-view-factors.md) | Explains `SkyViewFactor`, `HorizonViewFactor`, and how diffuse visibility fields are produced. | `POST /api/voxelShading/calculate`, `CalculateShadingRequest`, `VoxelShadingCalcParams` |
| [Incident radiation from weather and shading](incident-radiation.md) | Explains how EPW weather, surface orientation, sunlit fraction, SVF, and HVF are combined into incident solar radiation. | `Weather.ComputeAnnualIncidentRadiationFromShadingResult`, shading result outputs |
| [Sunlit fraction calculation](sunlit-fraction.md) | Explains representative-day sun vectors, ray marching, area-weighted group averaging, and output array shape. | `POST /api/voxelShading/calculate`, `GET /api/voxelShading/result/{jobId}` |
| [Voxelization, sensor generation, and shading pipeline](voxelization-sensors-calculation.md) | Explains the API workflow and options for LiDAR voxelization, sensor generation, shading calculation, previews, and polling. | `POST /api/voxelShading/voxelize`, `generateSensors`, `calculate`, previews |

## Source Map

| Topic | Main implementation files |
| --- | --- |
| Sky/horizon view factors | `EnergyAtlasCore/VoxelShading/SkyViewFactor.cs`, `EnergyAtlasCore/VoxelShading/HorizonViewFactor.cs` |
| Sunlit fraction | `EnergyAtlasCore/VoxelShading/ShadingCalculation.cs`, `EnergyAtlasCore/Geometry/SolarGeometry.cs` |
| Incident radiation | `EnergyAtlasCore/Weather.cs`, `EnergyAtlasCore/Model/PerezSky.cs` |
| LiDAR voxelization | `EnergyAtlasLib/Preprocessing/TiledLidarVoxelization.cs`, `EnergyAtlasLib/Preprocessing/TileSlicer.cs` |
| Sensor generation | `EnergyAtlasCore/VoxelShading/ShadingSensorGen.cs`, `EnergyAtlasLib/Preprocessing/TiledSensorGeneration.cs` |
| Web API | `EnergyAtlasWeb/Controllers/VoxelShadingController.cs` |
| Python API | `Connectors/python/src/energyatlas/client.py`, `Connectors/python/src/energyatlas/models.py` |

## API Reference Links

- The [Python API reference](../../python/index.md) links to this guide index and each guide above.
- The [Web API reference](../../web-api/index.md) links to this guide index and each guide above.
