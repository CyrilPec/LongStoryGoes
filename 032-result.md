
=================================================================
032 — SIMPLE TURNING MODEL
=================================================================

WORKPIECE
-----------------------------------------------------------------
Material:       AISI 1040
Diameter:       20.00 mm

TOOL
-----------------------------------------------------------------
Tool:           HSS
Section:        10.0 x 10.0 mm
Overhang:       30.0 mm

CUTTING PARAMETERS
-----------------------------------------------------------------
Depth of cut:   2.000 mm
Feed:           0.100 mm/rev
Cutting speed:  20.00 m/min

CALCULATED
-----------------------------------------------------------------
RPM:             318.31
Feed velocity:   31.83 mm/min
Chip area:       0.2000 mm²
Cutting force:   300.00 N
Torque:          3.000 N·m
Power:            100.00 W
MRR:              6.37 mm³/min

TOOL MECHANICS
-----------------------------------------------------------------
Tool moment:     9.000 N·m
Bending stress:  54.00 MPa

=================================================================

=================================================================
VERIFICATION
=================================================================
✓ RPM equation
✓ Cutting-force equation
✓ Power equation
✓ Material-removal-rate equation

All basic equations verified.

MODEL STATUS
-----------------------------------------------------------------
Geometry:       analytical
Chip model:     simplified
Force model:    Fc = Kc * Ac
Tool model:     cantilever beam
Dynamics:       not yet implemented
PyBullet:       next stage
Fields:         future stage

=== Code Execution Successful ===
