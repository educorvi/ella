# -*- coding: utf-8 -*-
# # Copyright (c) 2016-2025 educorvi GmbH & Co. KG
# # lars.walther@educorvi.de
import json
from collections import namedtuple
from .models import Welcome, ServiceDescription, GroupServiceDescription, FormDescription, UISchema, ServiceButton, MediaContainer, MediaFile
from .examples import example_services

def createForm(form):
    tst_name = 'test'
    tst_description = 'testdescription'
    ella_form = FormDescription(
            name = tst_name,
            title = form.get('title'),
            description = tst_description,
            type = 'object',
            properties = form.get('properties'),
            required = form.get('required'),
            )
    return ella_form

def createServiceButtons(formactions):
    ella_buttons = []
    for button in formactions:
        ella_button = ServiceButton(
                name = button.get('name'),
                title = button.get('title'),
                cssclass = button.get('cssclass'),
                method = button.get('method'))
        if button.get('additional'):
            ella_button.additional = button.get('additional')
        if button.get('modaltitle'):
            ella_button.modaltitle = button.get('modaltitle')
        if button.get('modaltext'):
            ella_button.modaltext = button.get('modaltext')
        ella_buttons.append(ella_button)
    return ella_buttons

def createFormService(service):
    form = json.loads(service.get('form'))
    ui = json.loads(service.get('ui'))
    ella_service = ServiceDescription(
            name = service.get('name'),
            title = service.get('title'),
            description = service.get('description'),
            type = 'service',
            form = createForm(form),
            ui = ui,
            formactions = createServiceButtons(service.get('formactions'))
            )
    return ella_service

def createPageService(service):
    ella_service = ServiceDescription(
            name = service.get('name'),
            title = service.get('title'),
            description = service.get('description'),
            type = 'page',
            text = service.get('text')
            )
    return ella_service

def createGroupFormService(service):
    ella_service = GroupServiceDescription(
            name = service.get('name'),
            title = service.get('title'),
            description = service.get('description'),
            type = 'service',
            form = createForm(service.get('form')),
            ui = UISchema(type = "VerticalLayout", elements = service.get('ui')),
            formactions = createServiceButtons(service.get('formactions'))
            )
    return ella_service

def createGroupPageService(service):
    ella_service = GroupServiceDescription(
            name = service.get('name'),
            title = service.get('title'),
            description = service.get('description'),
            type = 'page',
            text = service.get('text')
            )
    return ella_service   

def createGroupMediaService(service):
    ella_service = GroupServiceDescription(
            name = service.get('name'),
            title = service.get('title'),
            description = service.get('description'),
            type = 'media',
            media = createMediaContainer(service),
            )
    return ella_service

def createGroupService(service):
    ella_subservices = list()
    subservices = service.get('services')
    for subservice in subservices:
        typ = subservice.get('type')
        if typ == 'service':
            ella_subservices.append(createGroupFormService(subservice))
        elif typ in ['audio', 'video']:
            ella_subservices.append(createGroupMediaService(subservice))
        else:
            ella_subservices.append(createGroupPageService(subservice))
    ella_service = ServiceDescription(
            name = service.get('name'),
            title = service.get('title'),
            description = service.get('description'),
            type = 'group',
            services = ella_subservices
            )
    return ella_service

def createMediaFiles(files):
    ella_mediafiles = list()
    for mediafile in files:
        transcript = ''
        if mediafile.get('transcript'):
            if mediafile.get('mimetype') == 'audio/mpeg':
                transcript = mediafile.get('transcript').replace('\r\n', '\n')
        ella_mediafile = MediaFile(
                name = mediafile.get('name'),
                title = mediafile.get('title'),
                description = mediafile.get('description'),
                url = mediafile.get('url'),
                mimetype = mediafile.get('mimetype'),
                transcript = transcript,
                imageurl = mediafile.get('imageurl'),
                imagecaption = mediafile.get('imagecaption')
                )
        ella_mediafiles.append(ella_mediafile)
    return ella_mediafiles

def createMediaContainer(service):
    files = service.get('mediafiles')
    ella_mediafiles = createMediaFiles(files)
    media_container = MediaContainer(
            name = service.get('name'),
            title = service.get('title'),
            description = service.get('description'),
            type = service.get('type'),
            textbefore = service.get('textbefore'),
            textafter = service.get('textafter'),
            mediafiles = ella_mediafiles)
    return media_container

def createMediaService(service):
    ella_service = ServiceDescription(
            name = service.get('name'),
            title = service.get('title'),
            description = service.get('description'),
            type = 'media',
            media = createMediaContainer(service)
            )
    return ella_service

def ellaview2welcome(raw):
    services = raw.get('services')
    ella_services = list()
    for service in services:
        typ = service.get('type')
        if typ == 'group':
            ella_services.append(createGroupService(service))
        elif typ == 'service':
            ella_services.append(createFormService(service))
        elif typ == 'page':
            ella_services.append(createPageService(service))
        elif typ in ['audio', 'video']:
            ella_services.append(createMediaService(service))
    ella_welcome = Welcome(
        name = raw.get('name'),
        title = raw.get('title'),
        description = raw.get('description'),
        bodytext = raw.get('bodytext'),
        services = ella_services
        )
    return ella_welcome
