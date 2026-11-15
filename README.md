# Retail Concept Art

Abstract pieces for in-store display: 70 images, every one generated from code and rendered with Blender 5.3 Cycles (OptiX) on an NVIDIA RTX 5090.

**[View the gallery](https://rayhe.github.io/retail-concept-art/)**: the shareable web version, with a full-screen viewer.

**Full-resolution PNGs** (2400x3000 portrait, 3000x3000 square, 3840x2160 landscape) are attached to the [v1 release](../../releases/tag/v1). Click a thumbnail for a 1600 px preview.

## Re-render any piece

Each file name is `<number>-<piece>-s<seed>`. The piece and seed rebuild the same scene, palette and camera at any size (Blender 5.3):

```
blender -b --factory-startup -P generator/retail_scenes.py -- --piece podiums --seed 123456 --out podiums.png --samples 384 --scale 1.0
```

`--scale 2` doubles the resolution for large prints. Palettes: sand, blush, ocean, noir, citrus, lilac.

| Piece | What it is |
|---|---|
| arches | Sunlit plaster arches: a colonnade or corridor with long late-afternoon shadows. |
| podiums | Display podiums in marble, colour and brushed gold, topped with glass, rings and cubes. |
| ribbons | Satin and gold ribbons drifting across a seamless studio backdrop. |
| monoliths | Tinted glass slabs in front of a wall washed with two coloured lights. |
| spheres | A Fibonacci garden of gold, clay, frosted-glass and iridescent spheres. |
| waves | Dark silk: a folded surface grazed by coloured light. |

## Arches (12)

<p>
<a href="previews/005-arches-s252832.jpg"><img src="thumbs/005-arches-s252832.jpg" width="240" alt="arches, seed 252832, ocean palette" title="005-arches-s252832 (ocean, 2400x3000)"></a>
<a href="previews/010-arches-s514371.jpg"><img src="thumbs/010-arches-s514371.jpg" width="240" alt="arches, seed 514371, noir palette" title="010-arches-s514371 (noir, 2400x3000)"></a>
<a href="previews/017-arches-s812177.jpg"><img src="thumbs/017-arches-s812177.jpg" width="240" alt="arches, seed 812177, ocean palette" title="017-arches-s812177 (ocean, 2400x3000)"></a>
<a href="previews/020-arches-s440376.jpg"><img src="thumbs/020-arches-s440376.jpg" width="240" alt="arches, seed 440376, noir palette" title="020-arches-s440376 (noir, 2400x3000)"></a>
<a href="previews/027-arches-s152876.jpg"><img src="thumbs/027-arches-s152876.jpg" width="240" alt="arches, seed 152876, ocean palette" title="027-arches-s152876 (ocean, 2400x3000)"></a>
<a href="previews/034-arches-s332985.jpg"><img src="thumbs/034-arches-s332985.jpg" width="240" alt="arches, seed 332985, citrus palette" title="034-arches-s332985 (citrus, 2400x3000)"></a>
<a href="previews/037-arches-s805626.jpg"><img src="thumbs/037-arches-s805626.jpg" width="240" alt="arches, seed 805626, citrus palette" title="037-arches-s805626 (citrus, 2400x3000)"></a>
<a href="previews/045-arches-s843808.jpg"><img src="thumbs/045-arches-s843808.jpg" width="240" alt="arches, seed 843808, noir palette" title="045-arches-s843808 (noir, 2400x3000)"></a>
<a href="previews/054-arches-s996695.jpg"><img src="thumbs/054-arches-s996695.jpg" width="240" alt="arches, seed 996695, ocean palette" title="054-arches-s996695 (ocean, 2400x3000)"></a>
<a href="previews/055-arches-s949266.jpg"><img src="thumbs/055-arches-s949266.jpg" width="240" alt="arches, seed 949266, noir palette" title="055-arches-s949266 (noir, 2400x3000)"></a>
<a href="previews/062-arches-s346034.jpg"><img src="thumbs/062-arches-s346034.jpg" width="240" alt="arches, seed 346034, citrus palette" title="062-arches-s346034 (citrus, 2400x3000)"></a>
<a href="previews/068-arches-s607545.jpg"><img src="thumbs/068-arches-s607545.jpg" width="240" alt="arches, seed 607545, blush palette" title="068-arches-s607545 (blush, 2400x3000)"></a>
</p>

## Podiums (12)

<p>
<a href="previews/003-podiums-s958351.jpg"><img src="thumbs/003-podiums-s958351.jpg" width="240" alt="podiums, seed 958351, noir palette" title="003-podiums-s958351 (noir, 2400x3000)"></a>
<a href="previews/008-podiums-s576124.jpg"><img src="thumbs/008-podiums-s576124.jpg" width="240" alt="podiums, seed 576124, noir palette" title="008-podiums-s576124 (noir, 2400x3000)"></a>
<a href="previews/015-podiums-s687298.jpg"><img src="thumbs/015-podiums-s687298.jpg" width="240" alt="podiums, seed 687298, ocean palette" title="015-podiums-s687298 (ocean, 2400x3000)"></a>
<a href="previews/019-podiums-s401246.jpg"><img src="thumbs/019-podiums-s401246.jpg" width="240" alt="podiums, seed 401246, sand palette" title="019-podiums-s401246 (sand, 2400x3000)"></a>
<a href="previews/029-podiums-s763651.jpg"><img src="thumbs/029-podiums-s763651.jpg" width="240" alt="podiums, seed 763651, citrus palette" title="029-podiums-s763651 (citrus, 2400x3000)"></a>
<a href="previews/032-podiums-s684201.jpg"><img src="thumbs/032-podiums-s684201.jpg" width="240" alt="podiums, seed 684201, citrus palette" title="032-podiums-s684201 (citrus, 2400x3000)"></a>
<a href="previews/038-podiums-s337939.jpg"><img src="thumbs/038-podiums-s337939.jpg" width="240" alt="podiums, seed 337939, lilac palette" title="038-podiums-s337939 (lilac, 2400x3000)"></a>
<a href="previews/043-podiums-s834016.jpg"><img src="thumbs/043-podiums-s834016.jpg" width="240" alt="podiums, seed 834016, lilac palette" title="043-podiums-s834016 (lilac, 2400x3000)"></a>
<a href="previews/051-podiums-s607076.jpg"><img src="thumbs/051-podiums-s607076.jpg" width="240" alt="podiums, seed 607076, sand palette" title="051-podiums-s607076 (sand, 2400x3000)"></a>
<a href="previews/056-podiums-s820299.jpg"><img src="thumbs/056-podiums-s820299.jpg" width="240" alt="podiums, seed 820299, citrus palette" title="056-podiums-s820299 (citrus, 2400x3000)"></a>
<a href="previews/066-podiums-s831077.jpg"><img src="thumbs/066-podiums-s831077.jpg" width="240" alt="podiums, seed 831077, sand palette" title="066-podiums-s831077 (sand, 2400x3000)"></a>
<a href="previews/069-podiums-s966899.jpg"><img src="thumbs/069-podiums-s966899.jpg" width="240" alt="podiums, seed 966899, noir palette" title="069-podiums-s966899 (noir, 2400x3000)"></a>
</p>

## Ribbons (11)

<p>
<a href="previews/001-ribbons-s354859.jpg"><img src="thumbs/001-ribbons-s354859.jpg" width="240" alt="ribbons, seed 354859, citrus palette" title="001-ribbons-s354859 (citrus, 3840x2160)"></a>
<a href="previews/012-ribbons-s659923.jpg"><img src="thumbs/012-ribbons-s659923.jpg" width="240" alt="ribbons, seed 659923, lilac palette" title="012-ribbons-s659923 (lilac, 3840x2160)"></a>
<a href="previews/013-ribbons-s654338.jpg"><img src="thumbs/013-ribbons-s654338.jpg" width="240" alt="ribbons, seed 654338, citrus palette" title="013-ribbons-s654338 (citrus, 3840x2160)"></a>
<a href="previews/022-ribbons-s250296.jpg"><img src="thumbs/022-ribbons-s250296.jpg" width="240" alt="ribbons, seed 250296, sand palette" title="022-ribbons-s250296 (sand, 3840x2160)"></a>
<a href="previews/026-ribbons-s853839.jpg"><img src="thumbs/026-ribbons-s853839.jpg" width="240" alt="ribbons, seed 853839, citrus palette" title="026-ribbons-s853839 (citrus, 3840x2160)"></a>
<a href="previews/036-ribbons-s994113.jpg"><img src="thumbs/036-ribbons-s994113.jpg" width="240" alt="ribbons, seed 994113, ocean palette" title="036-ribbons-s994113 (ocean, 3840x2160)"></a>
<a href="previews/042-ribbons-s387867.jpg"><img src="thumbs/042-ribbons-s387867.jpg" width="240" alt="ribbons, seed 387867, noir palette" title="042-ribbons-s387867 (noir, 3840x2160)"></a>
<a href="previews/048-ribbons-s700666.jpg"><img src="thumbs/048-ribbons-s700666.jpg" width="240" alt="ribbons, seed 700666, ocean palette" title="048-ribbons-s700666 (ocean, 3840x2160)"></a>
<a href="previews/052-ribbons-s402765.jpg"><img src="thumbs/052-ribbons-s402765.jpg" width="240" alt="ribbons, seed 402765, blush palette" title="052-ribbons-s402765 (blush, 3840x2160)"></a>
<a href="previews/058-ribbons-s561211.jpg"><img src="thumbs/058-ribbons-s561211.jpg" width="240" alt="ribbons, seed 561211, ocean palette" title="058-ribbons-s561211 (ocean, 3840x2160)"></a>
<a href="previews/064-ribbons-s340170.jpg"><img src="thumbs/064-ribbons-s340170.jpg" width="240" alt="ribbons, seed 340170, ocean palette" title="064-ribbons-s340170 (ocean, 3840x2160)"></a>
</p>

## Monoliths (12)

<p>
<a href="previews/004-monoliths-s496598.jpg"><img src="thumbs/004-monoliths-s496598.jpg" width="240" alt="monoliths, seed 496598, ocean palette" title="004-monoliths-s496598 (ocean, 2400x3000)"></a>
<a href="previews/009-monoliths-s210923.jpg"><img src="thumbs/009-monoliths-s210923.jpg" width="240" alt="monoliths, seed 210923, ocean palette" title="009-monoliths-s210923 (ocean, 2400x3000)"></a>
<a href="previews/016-monoliths-s81581.jpg"><img src="thumbs/016-monoliths-s81581.jpg" width="240" alt="monoliths, seed 81581, ocean palette" title="016-monoliths-s81581 (ocean, 2400x3000)"></a>
<a href="previews/021-monoliths-s842613.jpg"><img src="thumbs/021-monoliths-s842613.jpg" width="240" alt="monoliths, seed 842613, sand palette" title="021-monoliths-s842613 (sand, 2400x3000)"></a>
<a href="previews/030-monoliths-s566131.jpg"><img src="thumbs/030-monoliths-s566131.jpg" width="240" alt="monoliths, seed 566131, citrus palette" title="030-monoliths-s566131 (citrus, 2400x3000)"></a>
<a href="previews/031-monoliths-s889623.jpg"><img src="thumbs/031-monoliths-s889623.jpg" width="240" alt="monoliths, seed 889623, citrus palette" title="031-monoliths-s889623 (citrus, 2400x3000)"></a>
<a href="previews/041-monoliths-s566661.jpg"><img src="thumbs/041-monoliths-s566661.jpg" width="240" alt="monoliths, seed 566661, citrus palette" title="041-monoliths-s566661 (citrus, 2400x3000)"></a>
<a href="previews/047-monoliths-s313396.jpg"><img src="thumbs/047-monoliths-s313396.jpg" width="240" alt="monoliths, seed 313396, citrus palette" title="047-monoliths-s313396 (citrus, 2400x3000)"></a>
<a href="previews/050-monoliths-s496282.jpg"><img src="thumbs/050-monoliths-s496282.jpg" width="240" alt="monoliths, seed 496282, ocean palette" title="050-monoliths-s496282 (ocean, 2400x3000)"></a>
<a href="previews/060-monoliths-s335547.jpg"><img src="thumbs/060-monoliths-s335547.jpg" width="240" alt="monoliths, seed 335547, noir palette" title="060-monoliths-s335547 (noir, 2400x3000)"></a>
<a href="previews/063-monoliths-s891711.jpg"><img src="thumbs/063-monoliths-s891711.jpg" width="240" alt="monoliths, seed 891711, blush palette" title="063-monoliths-s891711 (blush, 2400x3000)"></a>
<a href="previews/070-monoliths-s969768.jpg"><img src="thumbs/070-monoliths-s969768.jpg" width="240" alt="monoliths, seed 969768, sand palette" title="070-monoliths-s969768 (sand, 2400x3000)"></a>
</p>

## Spheres (11)

<p>
<a href="previews/002-spheres-s523746.jpg"><img src="thumbs/002-spheres-s523746.jpg" width="240" alt="spheres, seed 523746, lilac palette" title="002-spheres-s523746 (lilac, 2400x3000)"></a>
<a href="previews/011-spheres-s648807.jpg"><img src="thumbs/011-spheres-s648807.jpg" width="240" alt="spheres, seed 648807, lilac palette" title="011-spheres-s648807 (lilac, 3000x3000)"></a>
<a href="previews/018-spheres-s227274.jpg"><img src="thumbs/018-spheres-s227274.jpg" width="240" alt="spheres, seed 227274, ocean palette" title="018-spheres-s227274 (ocean, 3000x3000)"></a>
<a href="previews/024-spheres-s270760.jpg"><img src="thumbs/024-spheres-s270760.jpg" width="240" alt="spheres, seed 270760, sand palette" title="024-spheres-s270760 (sand, 2400x3000)"></a>
<a href="previews/025-spheres-s981055.jpg"><img src="thumbs/025-spheres-s981055.jpg" width="240" alt="spheres, seed 981055, ocean palette" title="025-spheres-s981055 (ocean, 3000x3000)"></a>
<a href="previews/035-spheres-s32990.jpg"><img src="thumbs/035-spheres-s32990.jpg" width="240" alt="spheres, seed 32990, noir palette" title="035-spheres-s32990 (noir, 3000x3000)"></a>
<a href="previews/040-spheres-s380860.jpg"><img src="thumbs/040-spheres-s380860.jpg" width="240" alt="spheres, seed 380860, citrus palette" title="040-spheres-s380860 (citrus, 3000x3000)"></a>
<a href="previews/046-spheres-s155385.jpg"><img src="thumbs/046-spheres-s155385.jpg" width="240" alt="spheres, seed 155385, lilac palette" title="046-spheres-s155385 (lilac, 3000x3000)"></a>
<a href="previews/053-spheres-s73153.jpg"><img src="thumbs/053-spheres-s73153.jpg" width="240" alt="spheres, seed 73153, noir palette" title="053-spheres-s73153 (noir, 2400x3000)"></a>
<a href="previews/059-spheres-s709538.jpg"><img src="thumbs/059-spheres-s709538.jpg" width="240" alt="spheres, seed 709538, noir palette" title="059-spheres-s709538 (noir, 2400x3000)"></a>
<a href="previews/061-spheres-s816749.jpg"><img src="thumbs/061-spheres-s816749.jpg" width="240" alt="spheres, seed 816749, lilac palette" title="061-spheres-s816749 (lilac, 2400x3000)"></a>
</p>

## Waves (12)

<p>
<a href="previews/006-waves-s605907.jpg"><img src="thumbs/006-waves-s605907.jpg" width="240" alt="waves, seed 605907, blush palette" title="006-waves-s605907 (blush, 3840x2160)"></a>
<a href="previews/007-waves-s582419.jpg"><img src="thumbs/007-waves-s582419.jpg" width="240" alt="waves, seed 582419, lilac palette" title="007-waves-s582419 (lilac, 3840x2160)"></a>
<a href="previews/014-waves-s917419.jpg"><img src="thumbs/014-waves-s917419.jpg" width="240" alt="waves, seed 917419, noir palette" title="014-waves-s917419 (noir, 3840x2160)"></a>
<a href="previews/023-waves-s144963.jpg"><img src="thumbs/023-waves-s144963.jpg" width="240" alt="waves, seed 144963, lilac palette" title="023-waves-s144963 (lilac, 3840x2160)"></a>
<a href="previews/028-waves-s426386.jpg"><img src="thumbs/028-waves-s426386.jpg" width="240" alt="waves, seed 426386, lilac palette" title="028-waves-s426386 (lilac, 3840x2160)"></a>
<a href="previews/033-waves-s242479.jpg"><img src="thumbs/033-waves-s242479.jpg" width="240" alt="waves, seed 242479, ocean palette" title="033-waves-s242479 (ocean, 3840x2160)"></a>
<a href="previews/039-waves-s609049.jpg"><img src="thumbs/039-waves-s609049.jpg" width="240" alt="waves, seed 609049, blush palette" title="039-waves-s609049 (blush, 3840x2160)"></a>
<a href="previews/044-waves-s362591.jpg"><img src="thumbs/044-waves-s362591.jpg" width="240" alt="waves, seed 362591, sand palette" title="044-waves-s362591 (sand, 3840x2160)"></a>
<a href="previews/049-waves-s703746.jpg"><img src="thumbs/049-waves-s703746.jpg" width="240" alt="waves, seed 703746, noir palette" title="049-waves-s703746 (noir, 3840x2160)"></a>
<a href="previews/057-waves-s350207.jpg"><img src="thumbs/057-waves-s350207.jpg" width="240" alt="waves, seed 350207, citrus palette" title="057-waves-s350207 (citrus, 3840x2160)"></a>
<a href="previews/065-waves-s529281.jpg"><img src="thumbs/065-waves-s529281.jpg" width="240" alt="waves, seed 529281, blush palette" title="065-waves-s529281 (blush, 3840x2160)"></a>
<a href="previews/067-waves-s236745.jpg"><img src="thumbs/067-waves-s236745.jpg" width="240" alt="waves, seed 236745, noir palette" title="067-waves-s236745 (noir, 3840x2160)"></a>
</p>

## License

The images, videos and generator code are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); see [LICENSE](LICENSE).
You may share and adapt them, including commercially, with credit: **&ldquo;Retail Concept Art by rayhe&rdquo;** and a link to https://github.com/rayhe/retail-concept-art.
