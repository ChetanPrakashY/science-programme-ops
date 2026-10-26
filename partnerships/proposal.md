# Three academic partnerships for a 5 m hyperspectral constellation

Prepared from the landscape in `../landscape/landscape.md` (OpenAlex data, Oct 2026).

## The gap

Between 2021 and 2026, OpenAlex lists 2,938 papers with an Indian author and "hyperspectral" in the
title or abstract. 51 of them use Italy's PRISMA satellite, 10 Germany's EnMAP, 8 DESIS, and 75 the
airborne AVIRIS-NG campaigns. **None mentions Pixxel.** The only research papers in OpenAlex that use
Pixxel data come from groups in Turkey/Malaysia, Greece and Australia, plus Pixxel's own calibration
paper (search for "pixxel", 12 records, Oct 2026).

Indian groups already know how to work with satellite hyperspectral data; they use foreign sensors at
30 m resolution. Firefly offers 5 m resolution, 135+ bands from 450 to 900 nm, and a 24-hour revisit
(pixxel.space/firefly, checked Oct 2026). For Indian fields, which are often smaller than a few 30 m
pixels, that difference is the reason to switch.

## 1. Crop traits at field scale: Banaras Hindu University

**Why them.** Prashant K. Srivastava's group at BHU (co-author on 5 of BHU's 6 spaceborne-sensor
papers in this data, some with IIT (BHU) colleagues) retrieves vegetation properties from satellite
hyperspectral data: crop traits from EnMAP with a PROSAIL radiative-transfer model
(doi:10.1016/j.jag.2025.104769) and a medicinal-plant compound mapped from PRISMA
(doi:10.1016/j.jag.2024.104202).

**Joint question.** Do crop traits retrieved at 5 m agree with field measurements on smallholder plots
better than at 30 m? The traits that depend mostly on the visible, red-edge and near-infrared
(chlorophyll, leaf area) fall inside Firefly's 450-900 nm range; traits that need the short-wave
infrared (leaf water) do not.

**What each side gets.** They get data at a resolution no public sensor offers and a paper; Pixxel gets
an independent, peer-reviewed validation in its largest market (agriculture), with field data.

## 2. A public benchmark dataset: IIT Bombay

**Why them.** IIT Bombay has the most hyperspectral output of any Indian university in this data (91
papers), with machine-learning work led by Biplab Banerjee (30 papers) and spectral geology by Alok K.
Porwal (23). Hyperspectral machine-learning research still leans on small airborne benchmark scenes
such as Indian Pines and Pavia University.

**Joint question.** Build and publish a labelled 5 m satellite hyperspectral benchmark over Indian
land cover, with a fixed train/test split and baseline results.

**What each side gets.** A benchmark paper is cited by everyone who uses it; every method paper that
follows puts Pixxel data in front of the machine-learning community. The data release has to go
through licensing and the publication review first.

## 3. Methods for VNIR geology and super-resolution: IIT Roorkee

**Why them.** IIT Roorkee has the most Indian papers using spaceborne hyperspectral sensors in this set
(15), mostly from Rahul Dev Garg's group: rock and mineral mapping with PRISMA and DESIS
(doi:10.1007/s10661-023-11200-1), dimensionality reduction, and super-resolution of PRISMA data
(doi:10.1080/01431161.2022.2114109).

**Joint question.** Their super-resolution and dimensionality-reduction work is directly useful: fuse
PRISMA's short-wave infrared with Firefly's 5 m VNIR. Firefly stops at 900 nm, so most alteration
minerals (which absorb in the short-wave infrared) are out of its range on its own; iron-oxide mapping
in the VNIR and the fusion question are in range. Being honest about this in the scoping call avoids a
project that cannot work.

**What each side gets.** A methods paper and a fusion approach Pixxel's mining customers can use.

## Also worth a first call

- Water quality: a Karunya University group used PRISMA for estuary water quality
  (doi:10.1007/s10661-023-11497-y), and water quality is one of Pixxel's own research topics.
- ISRO's Space Applications Centre and the Indian Institute of Remote Sensing are the largest
  producers here, but government agencies need a different kind of agreement than a university group.

## Next step

For each group: a one-page fit note and a first call, then the stages in `pipeline.md`.
