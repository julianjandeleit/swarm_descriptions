# Use the official Ubuntu 20.04 LTS as the base image
FROM ubuntu:20.04

# Set non-interactive environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    sudo \
    cmake \
    build-essential \
    libfreeimage-dev \
    libfreeimageplus-dev \
    qtbase5-dev \
    freeglut3-dev \
    libxi-dev \
    libxmu-dev \
    liblua5.2-dev \
    lua5.2 \
    doxygen \
    graphviz \
    graphviz-dev \
    asciidoc

# Set the installation directory
ENV ARGOS_INSTALL_PATH /opt/argos

# Create the installation directory
RUN mkdir -p $ARGOS_INSTALL_PATH

# Clone and install argos
WORKDIR /opt/argos
RUN git clone --branch 3.0.0-beta48 https://github.com/ilpincy/argos3.git argos3 \
    && cd argos3 \
    && mkdir build && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=$ARGOS_INSTALL_PATH/argos3-dist -DCMAKE_BUILD_TYPE=Release -DARGOS_INSTALL_LDSOCONF=OFF -DARGOS_DOCUMENTATION=OFF ../src \
    && make \
    && make install \
    && rm -rf $ARGOS_INSTALL_PATH/argos3-dist/include/argos3/plugins/robots/e-puck \
    && rm -rf $ARGOS_INSTALL_PATH/argos3-dist/lib/argos3/lib*epuck*.so

# Set environment variables
ENV PKG_CONFIG_PATH=$ARGOS_INSTALL_PATH/argos3-dist/lib/pkgconfig
ENV ARGOS_PLUGIN_PATH=$ARGOS_INSTALL_PATH/argos3-dist/lib/argos3
ENV LD_LIBRARY_PATH=$ARGOS_PLUGIN_PATH:$LD_LIBRARY_PATH
ENV PATH=$ARGOS_INSTALL_PATH/argos3-dist/bin/:$PATH

# Clone and install the e-puck plugin
WORKDIR /opt/argos
RUN git clone --branch v48 https://github.com/demiurge-project/argos3-epuck.git argos3-epuck \
    && cd argos3-epuck \
    && mkdir build && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=$ARGOS_INSTALL_PATH/argos3-dist -DCMAKE_BUILD_TYPE=Release ../src \
    && make \
    && make install

# Install AutoMoDe components
WORKDIR /opt/argos
# Clone experiments-loop-functions repository
RUN git clone https://github.com/demiurge-project/experiments-loop-functions.git AutoMoDe-loopfunctions \
    && cd AutoMoDe-loopfunctions \
    && mkdir build && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=$ARGOS_INSTALL_PATH/argos3-dist -DCMAKE_BUILD_TYPE=Release .. \
    && make

WORKDIR /opt/argos/AutoMoDe-loopfunctions
# Copy custom-loopfunctions directory into experiments-loop-functions repository
COPY custom-loopfunctions loop-functions/custom-loopfunctions
# Add custom-loopfunctions to CMakeLists.txt
RUN echo "add_subdirectory(custom-loopfunctions)" >> loop-functions/CMakeLists.txt

# Continue building experiments-loop-functions
RUN cd build \
    && make \
    && make install

WORKDIR /opt/argos
RUN git clone https://github.com/demiurge-project/demiurge-epuck-dao.git AutoMoDe-DAO \
    && cd AutoMoDe-DAO \
    && mkdir build && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=$ARGOS_INSTALL_PATH/argos3-dist -DCMAKE_BUILD_TYPE=Release .. \
    && make \
    && make install

WORKDIR /opt/argos
RUN git clone --branch BehaviorTree https://github.com/demiurge-project/ARGoS3-AutoMoDe.git AutoMoDe \
    && cd AutoMoDe \
    && mkdir build && cd build \
    && cmake .. \
    && make


# fix QT
RUN apt-get update && \
    apt-get install -y libqt5gui5 && \
    rm -rf /var/lib/apt/lists/*
ENV QT_DEBUG_PLUGINS=1

RUN apt-get update && apt-get install -y \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libxcb-xinerama0 \
    libxcb-xkb1

RUN apt-get update && apt-get install -y \
    libwayland-dev \
    libwayland-client0 \
    libwayland-server0
    
RUN apt-get update && apt-get install -y \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libwayland-dev \
    libwayland-client0 \
    libwayland-server0

RUN apt-get install -y gimp



#AutoMoDe-loopfunctions/
# Set the default command to start a shell
CMD ["/bin/bash"]
