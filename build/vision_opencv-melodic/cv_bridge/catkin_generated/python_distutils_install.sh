#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/bal/catkin_ws/src/vision_opencv-melodic/cv_bridge"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/bal/catkin_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/bal/catkin_ws/install/lib/python2.7/dist-packages:/home/bal/catkin_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/bal/catkin_ws/build" \
    "/usr/bin/python2" \
    "/home/bal/catkin_ws/src/vision_opencv-melodic/cv_bridge/setup.py" \
     \
    build --build-base "/home/bal/catkin_ws/build/vision_opencv-melodic/cv_bridge" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/bal/catkin_ws/install" --install-scripts="/home/bal/catkin_ws/install/bin"
