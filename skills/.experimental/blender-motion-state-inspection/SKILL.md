---
name: blender-motion-state-inspection
description: Inspect Blender characters, rigs, poses, retargeted animation, ground contact, facing direction, and model-vs-motion alignment using structured scene facts before relying on screenshots.
---

# Blender Motion State Inspection

Use this skill when a Blender avatar, armature, imported GLB/FBX, or retargeted animation may be twisted, mirrored, flattened, offset, foot-sliding, penetrating the floor, or facing the wrong direction.

## Principle

Do not judge animated 3D assets only from screenshots. Screenshots are review evidence, but they hide axis conventions, bone names, object scale, local transforms, parented meshes, material slots, and frame-by-frame contact state.

Extract structured Blender state first, then use viewport screenshots or renders to confirm what the facts imply.

## Workflow

1. Inventory the scene.
   - List meshes, armatures, empties, cameras, lights, modifiers, parent relationships, and hidden objects.
   - Separate character meshes from helper/proxy geometry before judging the avatar.
   - Record object-space and world-space bounding boxes.

2. Identify the skeleton.
   - Capture armature names, pose bones, bone heads/tails, roll, parent chains, constraints, and rest-pose axes.
   - Map semantic bones such as hips, spine, neck, head, shoulders, elbows, hands, thighs, knees, ankles, and feet.
   - Flag missing left/right pairs and unusual naming schemes.

3. Determine forward, up, and side axes.
   - Use pelvis, spine, shoulders, hips, head, and feet together; do not rely on a single mesh normal.
   - Compare local armature axes with world axes and imported file conventions such as glTF Y-up vs Blender Z-up.
   - Mark likely mirrored or backwards imports when face, feet, torso, and root motion disagree.

4. Sample animation frames.
   - Inspect first, middle, contact, airborne, and extreme frames.
   - Record root location, root heading, pelvis height, torso lean, limb directions, foot clearance, and mesh bounds.
   - For fast motion, sample more densely around flips, landings, turns, collisions, and floor contacts.

5. Check model integrity before retargeting blame.
   - Capture the clean baseline shape before applying animation.
   - Preserve original mesh, materials, armature, and skinning unless the user explicitly asks for repair.
   - Treat unexplained sphere-like blobs, giant proxy meshes, or crushed bodies as import/selection issues until proven otherwise.

6. Diagnose contact and motion issues.
   - Ground penetration: compare lowest foot or shoe vertices with floor height per frame.
   - Foot sliding: compare foot world positions across planted frames.
   - Leg crossover: compare left/right thigh, knee, ankle, and foot side ordering.
   - Twist damage: compare bone swing direction separately from roll/twist around the limb axis.
   - Scale drift: compare animated mesh bounds against the clean baseline bounds.

7. Report facts before opinions.
   - Include frame numbers, object names, bone names, world coordinates, and thresholds.
   - Separate confirmed failures from visual suspicions.
   - Attach screenshots only after the structured state explains what to look for.

## Output Template

```markdown
## Blender Motion Inspection

### Scene Inventory
- Character candidates:
- Armatures:
- Helper/proxy objects:
- Cameras/lights:

### Orientation
- World up:
- Character forward:
- Root heading:
- Mirrored/backwards risk:

### Baseline Integrity
- Clean mesh bounds:
- Animated mesh bounds:
- Materials/skin preserved:
- Suspicious non-character meshes:

### Frame Findings
| Frame | Finding | Evidence |
| --- | --- | --- |
| 1 | Clean baseline pose | hips/spine/feet aligned |
| 96 | Foot penetrates floor | left_foot min_z = -0.04 |

### Verdict
- Pass/fail:
- Required fix:
- Render readiness:
```

## Thresholds

- Treat ground penetration above 1-2 cm as visible unless the floor is soft or intentionally stylized.
- Treat a sudden scale change above 5% as likely rig, constraint, or transform inheritance trouble.
- Treat left/right ankle side-order flips during airborne inverted motion as leg crossover risk even if the pose recovers later.
- Treat root heading jumps above 30 degrees per frame as suspicious unless the source motion includes a snap turn.

## Anti-Patterns

- Do not modify body proportions to force pose matching unless the task is explicitly mesh repair.
- Do not bake away the clean baseline before recording it.
- Do not use one rendered camera angle as proof that a pose is correct.
- Do not delete helper objects until you have recorded why they are not part of the character.
- Do not assume an avatar faces +Y, -Y, +X, or -X without checking head, feet, torso, and root motion together.

## Tooling Notes

If a Blender state exporter is available, prefer JSON that includes meshes, armatures, pose bones, materials, contacts, bounding boxes, and sampled animation frames. If no exporter exists, run a small Blender Python script to collect those facts before proposing animation or retargeting fixes.
