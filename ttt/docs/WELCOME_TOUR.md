# Welcome Tour

This page will show you the structure of the project and where to find things. Read carefully so you'll be able to use even the _utility functions_ that this project provides.

<!-- TOC -->
* [Welcome Tour](#welcome-tour)
  * [1. Root folder](#1-root-folder)
  * [2. Module `/dronas2_partake`](#2-module-dronas2_partake)
    * [2.1 Detection](#21-detection)
    * [2.2 Analysis](#22-analysis)
    * [2.3 Mitigation](#23-mitigation)
  * [3 Module `/dronas2_partake/utils`](#3-module-dronas2_partakeutils)
    * [3.1 CpModels](#31-cpmodels)
<!-- TOC -->

## 1. Root folder

There are three main source folders in the project:

1. `/dronas2_partake`: Where the **library** stands.
3. `/test`: **Tests** and **examples** files of how to use this library.
4. `javainit.py`: used as a _shell_ for initializing the jvm.

_FYI_ other folders in the project are:

- `/docs`: is where this documentation resides.
- `/zres` is .gitignored and is used for config files such as the one that uses `DronasSession` class.

But from now we'll focus on `/dronas2_partake`.

## 2. Module `/dronas2_partake`

### 2.1 Detection

The detection algorithm is a function that enters a _list_ of `PartakeMission` and computes all the conflicts between them, so another _list_ of `PartakeConflict` is returned.

> **Warning:** To run the detection, you must have followed the instructions of installing the Java JDK in your computer.

### 2.2 Analysis

The analysis algorithm take a _list_ of `PartakeConflict` and splits them into independent clusters. 
In order to reduce the data used of run the following **mitigation** algorithm.

### 2.3 Mitigation

An optimizing *Constraint Programming* algorithm that mitigates all the conflicts in a traffic set
by delaying the take-off of the contained Missions (or cancelling them).

## 3 Module `/dronas2_partake/utils`

Interesting modules and functions to simplify some operations. The most highlighted ones are:

### 3.1 CpModels

Some base classes to let you implement a _Constraint Programming_ solution (using **Google OR-Tools**) and run it wrapped into a `with` or `for` statement, so the model is closed on exit.

It has two modes of running:
- **Simple:** wrapped in `with` statement, it waits until the final solution is computed to give it to you.
- **Multiple:** wrapped in a `for` loop, it performs an iteration every type a *feasible* solution that improves the previous one is found. Until the computation time is reached.
