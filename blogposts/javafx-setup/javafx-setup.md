---
layout: post
permalink: /
title: JavaFX Project Setup
post: 2518944094852483638
labels: Java,JavaFX,Jar
---

Outline:
- [X] Summary
    - [X] Build desktop application using JavaFX 
- [ ] Softwares used
    - [ ] IntelliJ Community Edition
    - [ ] Java
    - [ ] Maven
    - [ ] JavaFX SDK for Mac
    - [ ] Environement (Path and Java_home)
- [ ] Hello World (using IntelliJ)
    - [ ] Create using Maven archtype
    - [ ] Import in IntelliJ
    - [ ] Changes required to be done in settings of IntelliJ
    - [ ] Run, screenshot
    - [ ] Access Resources
        - [ ] frxml and css setup
        - [ ] Load Image from resources 
    - [ ] Run, screenshot
- [ ] Plugin to drag and drop components to build UI (Scene Builder https://www.jetbrains.com/help/idea/opening-fxml-files-in-javafx-scene-builder.html#open-in-scene-builder)
- [ ] Create fat Jar
    - [ ] Maven shade plugin to create executable Jar
- [ ] Template Project for JavaFX 
    - [ ] Create a template project in GitHub
- [ ] Closing 


## Introduction
Using JavaFX platform, we can build applications for desktop, mobile or embessed systems. It has large set of components to build rich user interface.

JavaFX allows,
- designing the user interface interactively using Scene Builder.
- testing the user inteface using TestFX.
- styling the user interface with the help of CSS.

JavaFX historically used to part of Java installation, however, now it is a standalone component which works on top of JDK. 

I faced multiple challenges during setting up the JavaFX with Java 21 to build a simple application recently. I would like to share the setup I ended up with which may help you as well.

We will be going to use following tools,
- [Java 21](https://docs.oracle.com/en/java/javase/21/index.html)
- [JavaFX SDK 22.0.2 (for MacOS)](https://gluonhq.com/products/javafx/)
- [Maven 3.8.3](https://maven.apache.org/download.cgi)
- [IntelliJ Idea](https://www.jetbrains.com/help/idea/installation-guide.html)

