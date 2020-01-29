#!/usr/bin/python3
"""cities api"""
from models import storage
from models.city import City
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


