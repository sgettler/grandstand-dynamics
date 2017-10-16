# Grandstand Dynamic Performance Check

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Performs analysis of grandstand structures to determine dynamic performance in
response to crowd action.

This software was developed for analysis of grandstands using SPS Terraces, but
is equally applicable to any structural system. The input to this application
is the solved mode shapes for the structure; tools and techniques for modeling
of the structural system are up to the user.

#### On Design Standards ####

This software is based on the recommendations of the [Institution of Structural
Engineers](https://www.istructe.org/) (IStructE) in their guideline, *Dynamic
Performance Requirements For Permanent Grandstands Subject To Crowd Action:
Recommendations for Management, Design and Assessment* (2008). The core of the
application is an implementation of the so-called "Route 2" method, based on
structural response to specified event scenarios.

The [American Institute of Steel Construction](https://www.aisc.org/) (AISC)
design guide, *Design Guide 11: Vibrations of Steel-Framed Structural Systems
Due to Human Activity (Second Edition)* (2016), now refers users to the
IStructE guideline for recommendations for evaluation of rhythmic excitation of
grandstands.
