---
layout: post
permalink: /
title: Build SVG in nodeJS
post: 2894909532221310478
labels: Javascript,svg
---

### Purpose
I noticed tags shown in Github with the help of link. That made me curious to know more about it. There are certain ways to do it but the interesting one I found was dynamically building and returing the SVG image which can directly render in markdown file. I came to know about [Shields](https://shields.io/) which builds beautiful dynamic badges as per the need.

### The Way
I wanted to create a basic setup which can render the tag directly in the markdown file. The first step was to create a svg content. We can do it in many ways, however to create dynamic tags I decided to go with nodeJS.

Building svg from scratch is quite tricky, I got to know about [Roughjs](https://roughjs.com/), which made things even simpler. Initial idea was to dynamically build tag as per the input sent in query parameter. It was a bit struggle initially to get it working. However, I came up with following function to achieve that.

With the help of monspace fonts, we can exactly calculate the width and height required for the tag. I tried to keep it as dynamically as possible.

```
const { DOMImplementation, XMLSerializer } = require('xmldom');
const xmlSerializer = new XMLSerializer();
const document = new DOMImplementation().createDocument('http://www.w3.org/1999/xhtml', 'html', null);

const rough = require('roughjs');

//...

function createSVG(text, color) {
    console.log(text);
    if(!text || text.length == 0) {
        text = '?';
    }

    if(text.length > maxTagSize) {
        text = text.substr(0, maxTagSize);
    }

    text = text.trim().toUpperCase();

    var textLength = text.length;

    var width = (fontWidth * textLength) + fontWidth;
    var height = fontSize * 1.5;

    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    const rc = rough.svg(svg);
    
    var tagName = document.createElementNS("http://www.w3.org/2000/svg", "text");
    tagName.setAttribute("x", (fontWidth / 2));
    tagName.setAttribute("y", fontSize + 1);
    tagName.setAttribute('style', 'font-family:monospace;font-weight:bold;font-size:'+fontSize+'px;');
    tagName.textContent = text;

    var rectangle = rc.rectangle(0, 0, width , height, {roughness: 0, fill : color, fillStyle: 'solid', stroke: '#8BD8E2'});
    
    svg.setAttribute("width", width);
    svg.setAttribute("height", height);
    svg.appendChild(rectangle);
    svg.appendChild(tagName);
    return svg;
}
```

Later I deployed this on Google Cloud Function to make it accessible for markdown by supplying function URL in HTML image tag source as shown below.

```
    <img src="https://tags.akashthakare.com/generateTag?title=java" />
```


### Next

This was a very interesting idea which I can publish and used in my own GitHub profile or even in readme files of repositories.

I would like to make it more interesting going forward. I am thinking to introduce icons or even images in it. This way it will give flexibility to caller of the function to build different styles of tag with different content. 

This can be implemented without using RoughJS. I will see if I can do it without using it. 

If you are interested, you can check the full code [here](https://github.com/aakashthakare/ghtag).