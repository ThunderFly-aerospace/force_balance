VPATH = $(SRC_DIR)

SOURCES=$(wildcard $(SRC_DIR)/*.scad)
AMF_TARGETS=$(patsubst $(SRC_DIR)/%.scad, $(AMF_DIR)/%.amf, $(SOURCES))
GCD_TARGETS=$(patsubst $(SRC_DIR)/%.scad, $(GCD_DIR)/%.gcode, $(SOURCES))

OPENSCAD?=openscad-nightly
SLICER?=~/Slic3r.AppImage

NAME_PREFIX?=''
SLIC3R_PROFILE?=''
PROCESSOR3D_PARAM?=
IMG_DIR?=''
PRINTER?=edee

RED=" \e[91m "
GRN=" \e[32m "
YEL=" \e[33m "
DEF=" \e[39m "

all: prepare_config default

prepare_config:
	@echo "Prepare config files for printer $(PRINTER)"
	@echo "git root: $(GIT_ROOT)"
	cd $(GIT_ROOT)CAD/slicing/; rm ./*.ini 2> /dev/null || true; cp -s 3dprinter_configs/dist/$(PRINTER)/*.ini .; ls .

default: $(AMF_TARGETS)
$(AMF_DIR)/%.amf: $(SRC_DIR)/%.scad
	@echo "\n\n"
	@echo $<
	@echo "\n"
	-processor3D \
		--output_folder $(GIT_ROOT)/$(OUTPUT_FOLDER) \
		--name_prefix $(NAME_PREFIX) \
		$(PROCESSOR3D_PARAM) $<
