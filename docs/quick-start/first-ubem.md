# Build Your First UBEM with EnergyAtlas

This tutorial will guide you through creating your first Urban Building Energy Model (UBEM) using EnergyAtlas.

## Prerequisites

Before starting, ensure you have:

- EnergyAtlas installed ([Installation Guide](installation.md))
- Basic understanding of UBEM concepts ([UBEM Fundamentals](ubem-fundamentals.md))
- Building data for your study area (building footprints, assessor data, or similar)

## Step 1: Prepare Your Data

### Required Data

- **Building footprints**: Shapefile or GeoJSON with building geometry
- **Building attributes**: Age, use type, floor area, number of stories
- **Weather data**: TMY or EPW weather file for your location

### Data Preparation

1. Organize your building data into a single file
2. Ensure coordinate system is consistent (preferably WGS84 or local UTM)
3. Clean data: remove duplicates, fix geometry errors
4. Validate attribute fields

**Learn more**: [Data Preparation Guide](../workflows/data-prep.md)

## Step 2: Create a New Project

1. Open EnergyAtlas
2. Click "New Project"
3. Enter project name and location
4. Select coordinate system matching your data

## Step 3: Import Building Data

1. Navigate to **Urban Data Integration** workflow
2. Click "Import Data"
3. Select your building footprint file
4. Map attribute fields to EnergyAtlas data model
5. Review imported buildings

**Learn more**: [Urban Data Integration Workflow](../workflows/gui/urban-data-integration.md)

## Step 4: Assign Building Archetypes

1. Navigate to **Template Definition and Assignment** workflow
2. Browse available archetypes from the library
3. Create assignment rules based on building characteristics
4. Review and adjust assignments as needed

**Learn more**: 
- [Template Definition and Assignment Workflow](../workflows/gui/template-definition-assignment.md)
- [Archetype Library](../library/resources/archetypes.md)

## Step 5: Run Simulation

1. Navigate to **Running and Calibrating** workflow
2. Select weather file for your location
3. Configure simulation parameters
4. Click "Run Simulation"
5. Monitor progress

**Learn more**: [Running and Calibrating Workflow](../workflows/gui/running-calibrating.md)

## Step 6: View Results

1. Navigate to **Results View** workflow
2. Explore energy consumption by:
   - Building use type
   - Building age
   - Geographic location
3. Export results for further analysis

**Learn more**: [Results View Workflow](../workflows/gui/results-view.md)

## Next Steps

- **Create Scenarios**: Model retrofit measures and policy scenarios
  - [Scenario Design and Simulation Workflow](../workflows/gui/scenario-design-simulation.md)
- **Calibrate Model**: Improve accuracy using observed data
  - [Running and Calibrating Workflow](../workflows/gui/running-calibrating.md)
- **Explore Advanced Features**: 
  - [EnergyAtlas Objects Guide](../library/objects/index.md)
  - [Technical References](../library/technical-references.md)

## Troubleshooting

Common issues and solutions:

- **Import errors**: Check data format and coordinate system
- **Missing archetypes**: Create custom archetypes or use library templates
- **Simulation failures**: Verify weather file compatibility and building assignments

**Need help?** Open an [issue on GitHub](https://github.com/Energy-Atlas/energy-atlas.github.io/issues/new).
