#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

# python rayTracer.py scenes/one-sphere.xml
# python rayTracer.py scenes/four-spheres.xml

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 


class Color:
    def __init__(self, R, G, B):
        self.color = np.array([R,G,B]).astype(np.float64)

    def __init__(self, colorArray):
        self.color = colorArray.astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)
    
class Light:
    def __init__(self) -> None:
        self.position = np.array([0, 0, 0]).astype(np.float64)
        self.intensity = np.array([1, 1, 1]).astype(np.float64)
    
class Shader:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type

    def set_color(self, diffuseColor, specularColor, exponent):
        self.dcolor = Color(diffuseColor)
        self.scolor = Color(specularColor)
        self.exponent = exponent

class Ray:
    def __init__(self, point, vector):
        self.p = point
        self.d = normalized_vector(vector)

class Sphere:
    def __init__(self, center, radius, shader):
        self.c = center
        self.r = radius
        self.shader = shader

class Intersection:
    def __init__(self, ray, sphere) -> None:
        self.time = get_distance(ray, sphere)
        self.point = ray.p + self.time * ray.d
        self.shader = sphere.shader
        normal = self.point - sphere.c
        self.normal = normalized_vector(normal)

    def shade(self, ray):
        v = -ray.d
        l = normalized_vector(light.position - self.point)
        h = normalized_vector(v + l)
        lightray = Ray(self.point, l)

        color = np.array([0, 0, 0]).astype(np.float64)

        blocked = 0
        for sphere in spheres:
            if discriminant(lightray, sphere) < 0:
                continue
            time = get_distance(lightray, sphere)
            if time > 0:
                blocked = 1

        # if blocked:
        #     return color

        color += max(np.dot(self.normal, l), 0) * light.intensity * self.shader.dcolor.color
        color += np.power(max(np.dot(self.normal, h), 0), self.shader.exponent) * light.intensity * self.shader.scolor.color

        return color


# global object
spheres = list()
shaders = dict()
light = Light()
max_distance = 0


def discriminant(ray, sphere):
    d = ray.d
    p = ray.p - sphere.c
    return np.power(np.dot(d, p), 2) - np.dot(d, d) * (np.dot(p, p) - np.power(sphere.r, 2))


def get_distance(ray, sphere):
    d = ray.d
    p = ray.p - sphere.c
    return (-1) * np.dot(d, p) - np.power(discriminant(ray, sphere), 1 / 2)


def normalized_vector(d):
    return (1 / np.linalg.norm(d)) * d


def reflected_vector(d, normal):
    cos = np.dot(d, normal)
    return 2 * cos * normal - d


def trace(ray):
    
    color = np.array([0, 0, 0])
    times = dict()
    min_distance = max_distance
    for sphere in spheres:
        if discriminant(ray, sphere) < 0:
            continue
        distance = get_distance(ray, sphere)
        if distance > 0:
            min_distance = min(min_distance, distance)
            times[distance] = sphere

    if len(times) == 0:
        return color
    
    sphere = times[min_distance]

    # calculate the color with light shading

    hit = Intersection(ray, sphere)
    color = hit.shade(ray)

    # calculate the color with the return value of the reflected ray

    # r = reflected_vector(-ray.d, hit.normal)
    # newray = Ray(hit.point, r)
    # if hit.shader.type == 'Phong':
    # return color + hit.shader.scolor.color * trace(newray)

    return color


def main():
    global max_distance
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float64)
    viewUp=np.array([0,1,0]).astype(np.float64)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float64)  # how bright the light is.

    imgSize=np.array(root.findtext('image').split()).astype(np.int32)

    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float64)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float64)
        viewDir = normalized_vector(viewDir)
        viewCross = normalized_vector(np.cross(viewDir, viewUp))
        viewUp = normalized_vector(np.cross(viewCross, viewDir))
        if c.findtext('projDistance'):
            projDistance = float(c.findtext('projDistance'))
        viewWidth = float(c.findtext('viewWidth'))
        viewHeight = float(c.findtext('viewHeight'))
    for c in root.findall('shader'):
        shader = Shader(c.get('name'), c.get('type'))
        diffuseColor = np.array(c.findtext('diffuseColor').split()).astype(np.float64)
        specularColor = np.array([0, 0, 0])
        exponent = 0
        if (shader.type == 'Phong') :
            specularColor = np.array(c.findtext('specularColor').split()).astype(np.float64)
            exponent = float(c.findtext('exponent'))
        shader.set_color(diffuseColor, specularColor, exponent)
        shaders[shader.name] = shader
    for c in root.findall('surface'):
        shader = shaders[c.find('shader').attrib['ref']]
        center = np.array(c.findtext('center').split()).astype(np.float64)
        radius = float(c.findtext('radius'))
        sphere = Sphere(center, radius, shader)
        spheres.append(sphere)
        distance = np.linalg.norm(center - viewPoint) + radius
        max_distance = max(max_distance, distance)
    for c in root.findall('light'):
        light.position = np.array(c.findtext('position').split()).astype(np.float64)
        light.intensity = np.array(c.findtext('intensity').split()).astype(np.float64)

        
    #code.interact(local=dict(globals(), **locals()))  

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0

    # replace the code block below!

    origin_of_image = viewPoint + projDistance * viewDir - (viewWidth / 2) * viewCross + (viewHeight / 2) * viewUp

    for i in np.arange(imgSize[1]): 
        for j in np.arange(imgSize[0]):

            dx = viewWidth * ((2 * j + 1) / 2) / imgSize[0]
            dy = viewHeight * ((2 * i + 1) / 2) / imgSize[1]
            coordinate = origin_of_image + dx * viewCross - dy * viewUp
            ray = Ray(viewPoint, coordinate - viewPoint)
            color = Color(trace(ray))
            color.gammaCorrect(2.2)
            img[i][j] = color.toUINT8()

    rawimg = Image.fromarray(img, 'RGB')
    rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
