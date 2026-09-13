#!/usr/bin/env bash
# Assemble the M2 steel-core video: frame sequences + ElevenLabs VO -> mp4
set -e
cd "$(dirname "$0")"
FB='C\:/Windows/Fonts/arialbd.ttf'
FR='C\:/Windows/Fonts/arial.ttf'
mkdir -p seg
dur() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }

# title(big, small) -> drawtext filter chain
title() {
  echo "drawtext=fontfile='$FB':text='$1':x=90:y=h-190:fontsize=58:fontcolor=white:alpha='min(1,max(0,(t-0.4)*1.6))',drawtext=fontfile='$FR':text='$2':x=92:y=h-118:fontsize=34:fontcolor=0xC9D1D9:alpha='min(1,max(0,(t-0.9)*1.6))'"
}

seg() { # seg <n> <clip> <voclip> <big> <small>
  local n=$1 clip=$2 vo=$3 big=$4 small=$5
  local d; d=$(dur "vo/$vo.mp3")
  ffmpeg -y -loglevel error -stream_loop -1 -i "clips/$clip.mp4" -t "$d" \
    -vf "$(title "$big" "$small")" -c:v libx264 -pix_fmt yuv420p -crf 19 -r 24 "seg/$n.mp4"
  printf "  %-4s %-9s %6.1fs  %s\n" "$n" "$clip" "$d" "$big"
}

echo "building segments"
seg 01 hero    01_hook     "Airsoft M2 replica — steel core" "full scale, 6 mm BBs, mostly 3D printed"
seg 02 explode 02_problem  "The problem"                    "a printed receiver this size flexes"

# 03 is the reveal: full gun crossfading to steel only
D3=$(dur vo/03_idea.mp3)
H=$(python -c "print(f'{($D3/2):.3f}')" 2>/dev/null || awk "BEGIN{printf \"%.3f\", $D3/2}")
ffmpeg -y -loglevel error -stream_loop -1 -i clips/hero.mp4 -stream_loop -1 -i clips/steel.mp4 \
  -filter_complex "[0:v]trim=duration=$(awk "BEGIN{printf \"%.3f\", $H+1.2}"),setpts=PTS-STARTPTS[a];\
[1:v]trim=duration=$(awk "BEGIN{printf \"%.3f\", $D3-$H+1.2}"),setpts=PTS-STARTPTS[b];\
[a][b]xfade=transition=fade:duration=1.2:offset=$(awk "BEGIN{printf \"%.3f\", $H}")[x];\
[x]trim=duration=$D3,setpts=PTS-STARTPTS,$(title "One piece of steel" "2 x 3 inch tube, 0.120 inch wall, 23 inches long")[v]" \
  -map "[v]" -c:v libx264 -pix_fmt yuv420p -crf 19 -r 24 seg/03.mp4
printf "  %-4s %-9s %6.1fs  %s\n" "03" "reveal" "$D3" "One piece of steel"

seg 04 steel   04_steel    "Everything that is metal"       "11.2 lb, all standard imperial stock"
seg 05 section 05_section  "In section"                     "PolarStar F2 with the direct-attach combo hop-up"
seg 06 ch      06_charging "Charging handle"                "150 mm of travel, spring returned"
seg 07 trig    07_trigger  "Trigger"                        "pivots on a pin through both tube walls"
seg 08 barrel  08_barrel   "Barrel is 1 inch EMT conduit"   "2 set screws, hex key reaches through the jacket"
seg 09 barrel  09_jacket   "The perforated jacket"          "the one part of the barrel worth printing"

# 10 outro carries the attribution card as well
D10=$(dur vo/10_outro.mp3)
ffmpeg -y -loglevel error -stream_loop -1 -i clips/hero.mp4 -t "$D10" \
  -vf "$(title "Files on GitHub" "github.com/erichexter/m2-airsoft-steel-core"),\
drawtext=fontfile='$FR':text='Skin geometry derived from HappyBattleSheep M2 on Thingiverse, CC BY':x=92:y=h-72:fontsize=26:fontcolor=0x8B949E:alpha='min(1,max(0,(t-16)*0.8))',\
drawtext=fontfile='$FR':text='Steel design CC BY-NC-SA 4.0   ·   airsoft replica, check local law':x=92:y=h-40:fontsize=26:fontcolor=0x8B949E:alpha='min(1,max(0,(t-18)*0.8))'" \
  -c:v libx264 -pix_fmt yuv420p -crf 19 -r 24 seg/10.mp4
printf "  %-4s %-9s %6.1fs  %s\n" "10" "hero" "$D10" "Files on GitHub"

echo "concatenating"
: > seg/list.txt
for n in 01 02 03 04 05 06 07 08 09 10; do echo "file '$n.mp4'" >> seg/list.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i seg/list.txt -c copy video_only.mp4

: > vo/list.txt
for f in vo/0*.mp3 vo/10_outro.mp3; do echo "file '$(basename "$f")'" >> vo/list.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i vo/list.txt -c copy narration.mp3

echo "muxing"
ffmpeg -y -loglevel error -i video_only.mp4 -i narration.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest M2_steel_core.mp4

echo
echo "video  $(dur video_only.mp4)s"
echo "audio  $(dur narration.mp3)s"
echo "final  $(dur M2_steel_core.mp4)s   $(du -h M2_steel_core.mp4 | cut -f1)"
