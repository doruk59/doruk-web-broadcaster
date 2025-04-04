#!/bin/bash

# Kill any existing ffmpeg processes
pkill -f ffmpeg

# YouTube streaming settings
RTMP_URL="rtmp://a.rtmp.youtube.com/live2/wq9u-uucb-0be2-3ys3-eg5e"
VIDEO_PATH="/media/doruk/KINGSTON"
LOGO_PATH="/media/doruk/KINGSTON/logo.png"

# Parse arguments
PLAYLIST_FILE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --playlist)
            PLAYLIST_FILE="$2"
            shift
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Create playlist file
if [ -n "$PLAYLIST_FILE" ] && [ -f "playlists/$PLAYLIST_FILE.json" ]; then
    # Parse JSON playlist and create ffmpeg concat file
    echo "ffconcat version 1.0" > playlist.txt
    python3 -c "
import json
with open('playlists/$PLAYLIST_FILE.json') as f:
    data = json.load(f)
    for video in data['videos']:
        print(f\"file '{video['path']}'\")" >> playlist.txt
    
    # Get play mode
    PLAY_MODE=$(python3 -c "
import json
with open('playlists/$PLAYLIST_FILE.json') as f:
    print(json.load(f)['play_mode'])")
else
    # Default playlist with all videos
    echo "ffconcat version 1.0" > playlist.txt
    for i in {001..010}; do
        echo "file '$VIDEO_PATH/$i.mp4'" >> playlist.txt
    done
    PLAY_MODE="loop"
fi

# Prepare FFmpeg options based on play mode
case $PLAY_MODE in
    "loop")
        LOOP_OPT="-stream_loop -1"
        ;;
    "once")
        LOOP_OPT=""
        ;;
    "random")
        # Shuffle playlist
        sort -R playlist.txt -o playlist.txt
        LOOP_OPT="-stream_loop -1"
        ;;
    *)
        LOOP_OPT="-stream_loop -1"
        ;;
esac

# Start streaming with ffmpeg
ffmpeg -re \
    -hwaccel v4l2m2m \
    -thread_queue_size 512 \
    $LOOP_OPT \
    -f concat -safe 0 -i playlist.txt \
    -i "$LOGO_PATH" \
    -filter_complex "[0:v][1:v]overlay=10:10" \
    -c:v h264_v4l2m2m \
    -preset veryfast \
    -b:v 4500k \
    -c:a aac -ar 44100 -b:a 128k \
    -f flv "$RTMP_URL"
