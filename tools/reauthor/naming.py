# Holistic naming for the M2 steel-core model.
#
#   <class>-<NN>-<Descriptive-Name>[-L|-R]
#
#   ST  steel you cut and weld
#   HW  hardware you buy (conduit, pins, switch)
#   PR  part you 3D print
#   RF  reference only - never built
#
# Number groups: 0x structure, 1x receiver skins, 2x barrel, 3x grips,
# 4x charging handle, 5x trigger, 6x engine.
#
# HANDEDNESS: -L / -R are the PHYSICAL sides of the gun, standing behind it
# firing forward (the muzzle is +X). The charging handle is on the right of a
# real M2 and sits at NEGATIVE Y here, so negative Y is the right-hand side.
# The donor mesh names have this backwards - its "Side_L*" parts are physically
# on the RIGHT. Every renamed part below follows the physical side.

COMPONENTS = {
    '1729 - F2 V2 M4 Solid Model for External Dimensions_objects': '00_Ref_PolarStar_F2',
    '2431 - Rev 3 FCU - Rev G_objects': '00_Ref_FCU',
    'Reference_Parts':   '00_Ref_Donor_Meshes',
    'Printed_Skins':     '00_Ref_Donor_Skins',
    'Barrel_Jacket':     '00_Ref_Donor_Jacket',
    'Rear_Grip':         '00_Ref_Donor_Grip',
    'Core_Box_2x3_11ga': '10_Steel_Core',
    'Steel_Weldments':   '11_Steel_Weldments',
    'Engine_Cradle':     '70_Print_Engine',
    'Charging_Handle':   '50_Print_Charging',
    'Trigger_Group':     '60_Print_Trigger',
}

# body name -> (new name, target component). 'HAND' means resolve -L/-R from Y.
BODIES = {
    # --- steel ------------------------------------------------------------
    'CoreBox_cut':            ('ST-01-Core-Tube',        '10_Steel_Core'),
    'Backplate_1-8':          ('ST-02-Backplate',        '11_Steel_Weldments'),
    'BP_Boss_L_1-2':          ('ST-03-Backplate-Boss',   '11_Steel_Weldments', 'HAND'),
    'BP_Boss_R_1-2':          ('ST-03-Backplate-Boss',   '11_Steel_Weldments', 'HAND'),
    'Barrel_Plate_1-4':       ('ST-04-Barrel-Plate',     '11_Steel_Weldments'),
    'Barrel_Socket_1-5x156':  ('ST-05-Barrel-Socket',    '11_Steel_Weldments'),
    'Hatch_Spine_1-8':        ('ST-06-Cover-Spine',      '11_Steel_Weldments'),
    'Hinge_Tab_L_1-8':        ('ST-07-Hinge-Tab',        '11_Steel_Weldments', 'HAND'),
    'Hinge_Tab_R_1-8':        ('ST-07-Hinge-Tab',        '11_Steel_Weldments', 'HAND'),
    'Pintle_Tab_L_1-2':       ('ST-08-Pintle-Tab',       '11_Steel_Weldments', 'HAND'),
    'Pintle_Tab_R_1-2':       ('ST-08-Pintle-Tab',       '11_Steel_Weldments', 'HAND'),
    # --- bought hardware ---------------------------------------------------
    'Barrel_EMT_1in':         ('HW-01-Barrel-EMT-1in',   '11_Steel_Weldments'),
    'REF_Switch_SS5GL13':     ('HW-02-Switch-SS5GL13',   '60_Print_Trigger'),
    'REF_PivotPin_4mm':       ('HW-03-Trigger-Pin-4mm',  '60_Print_Trigger'),
    # --- printed -----------------------------------------------------------
    'Side_R1_native':         ('PR-11-Side-Rear',        '20_Print_Receiver', 'HAND'),
    'Side_L1_native':         ('PR-12-Side-Rear',        '20_Print_Receiver', 'HAND'),
    'Side_R2_native':         ('PR-13-Side-Front',       '20_Print_Receiver', 'HAND'),
    'Side_L2_native':         ('PR-14-Side-Front',       '20_Print_Receiver', 'HAND'),
    'Top1_native':            ('PR-15-Top-Deck',         '20_Print_Receiver'),
    'Hatch_native':           ('PR-16-Top-Cover',        '20_Print_Receiver'),
    'FrontBoss_native':       ('PR-17-Front-Sight-Boss', '20_Print_Receiver'),
    'Bot1':                   ('PR-18-Bottom-Rear',      '20_Print_Receiver'),
    'Bot2':                   ('PR-19-Bottom-Front',     '20_Print_Receiver'),
    'Barrel_Jacket_Native':   ('PR-21-Barrel-Jacket',    '30_Print_Barrel'),
    'Grip_Assembly_native':   ('PR-31-Spade-Grips',      '40_Print_Grip'),
    'CH_Handle_native':       ('PR-41-CH-Handle',        '50_Print_Charging'),
    'CH_Carrier':             ('PR-42-CH-Carrier',       '50_Print_Charging'),
    'CH_Shoe':                ('PR-43-CH-Shoe',          '50_Print_Charging'),
    'Trigger':                ('PR-51-Trigger-Butterfly','60_Print_Trigger'),
    'Trigger_Switch_Carrier': ('PR-52-Trigger-Switch-Carrier', '60_Print_Trigger'),
    'Cradle_F2_HopUp':        ('PR-61-Engine-Cradle',    '70_Print_Engine'),
    # --- donor meshes, kept for reference only -----------------------------
    'Hatch':      ('RF-10-Donor-Top-Cover',   None),
    'Top1':       ('RF-11-Donor-Top-Deck',    None),
    'FrontBoss':  ('RF-12-Donor-Front-Boss',  None),
    'Side_L1':    ('RF-13-Donor-Side-Rear-R', None),
    'Side_R1':    ('RF-14-Donor-Side-Rear-L', None),
    'Side_L2':    ('RF-15-Donor-Side-Front-R',None),
    'Side_R2':    ('RF-16-Donor-Side-Front-L',None),
    'Barrel_Jacket': ('RF-17-Donor-Barrel-Jacket', None),
    'Grip_Assembly': ('RF-18-Donor-Spade-Grips',   None),
    'CH_Handle':  ('RF-19-Donor-CH-Handle',   None),
    'CH_ref':     ('RF-20-Donor-CH-Assembly', None),
    'trigger':    ('RF-21-Donor-Trigger',     None),
}

NEW_COMPONENTS = ('20_Print_Receiver', '30_Print_Barrel', '40_Print_Grip')

# components whose whole purpose is gone - the failed butterfly loft
DROP_COMPONENTS = ('Trig_Native',)

# native components emptied by the move; drop them once their body has left
EMPTIED = ('Jacket_Native', 'Hatch_Native', 'Top1_Native', 'Side_L2_Native',
           'Side_R2_Native', 'Side_L1_Native', 'Side_R1_Native',
           'FrontBoss_Native', 'CH_Handle_Native', 'Grip_Native')
