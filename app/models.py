# -*- coding: utf-8 -*-
# # Copyright (c) 2016-2021 educorvi GmbH & Co. KG
# # lars.walther@educorvi.de

from typing import Optional, List, Dict, Text, Union
from pydantic import BaseModel

class UISchema(BaseModel):
    type : str
    elements : List[dict]

class PDFData(BaseModel):
    form : dict

class FormDescription(BaseModel):
    """
    Beschreibung eines Formulars
    ============================

    Funktionen im ella ecosystem
    ----------------------------
    - Aufruf eines **ella_service** durch die **ella_app**:
        - Die Formularbeschreibung wird als {JSON-Schema} zurückgeliefert. Mit der
          Formularbeschreibung kann die **ella_app** das Formular anzeigen (engl. rendern).
    - Aufruf einer **ella_method** durch die **ella_app**:
        - Die Daten werden von der **ella_app** im {JSON-Format} passend zur
          Formularbeschreibung übergeben. Die eingehenden Daten werden mittels {JSON-Schema}
          validiert.

    Bechreibung der Attribute
    -------------------------
    - "name" = ID des Formulars
    - "title" = Titel des Formulars
    - "description" = Kurzbeschreibung des Formulars
    - "type" = 'object'
    - "properties" = Python-Dictionary zur Beschreibung der Formularfelder
    - "required" = Liste mit Pflichtfeldern des Formualars
    """
    name : Text
    title : Text
    description: Text
    type: str
    properties : Dict[str, dict]
    required : List[str]


class ServiceButton(BaseModel):
    """
    Beschreibung eines Buttons für den ella_service
    -----------------------------------------------
    - "name" = Name oder ID des Buttons
    - "title" = Beschriftung des Buttons
    - "cssclass" = Farbe und Aussehen des Buttons
    - "method" = HTTP-Methode zum Aufruf des Service [GET, POST, PUT]
    """
    name: str
    title: Text
    cssclass: str
    method: str


class ServiceDescription(BaseModel):
    """
    Beschreibung eines Services (ella_service) für die ella_app
    -----------------------------------------------------------
    - "title" = Titel des Service oder der Gruppe
    - "description" = Kurzbeschreibung des Service oder der Gruppe
    - "type" = Das Attribut type hat folgende Optionen:
        * "page" = Es wird eine Seite angezeigt. Der Richtext der Seite steht im Attribut "text"
        * "form" = Es wird ein Formular angezeigt. Das JSON-Schema des Formulars steht im Attribut "form"
        * "group" = Es handelt sich um eine Gruppe von Services. Die Services stehen dann in "services"
    - "text" = optional (bei type=page): <HTML> Richtext der Seite
    - "form" = optional (bei type=form): JSON-Schema der Form
    - "ui" = optional (bei type=form): UI-Schema der Form
    - "services" = optional (bei type=group): Liste mit weiteren Servicebeschreibungen
    - "formactions" = optional: Liste mit Form Actions (Buttons)
    """
    name : Text
    title : Text
    description : Text
    type: str #page, service, group
    text : Optional[Text]
    form : Optional[FormDescription]
    ui : Optional[UISchema]
    services : Optional[List[str]]
    formactions : Optional[List[ServiceButton]]


class Welcome(BaseModel):
    """
    Beschreibung einer Welcome-Page für die ella_app
    ------------------------------------------------

    - "title" = Titel der **ella_app**
    - "description = Kurzbeschreibung der **ella_app**
    - "bodytext" = <HTML> RichText mit den Inhalten der Welcome-Page
    - "services" = Listen mit den Servicebeschreibungen der **ella_services** (class: ServiceDescription)
    - "impressum" = <HTML> Richtext mit den Inhalten des Impressums
    - "privacy" = <HTML> Richtext mit den Inhalten der Datenschutzinformation
    - "contact" = Servicebeschreibung oder <HTML> Richtext
    """
    name : Text
    title : Text
    description : Text
    bodytext : Text
    services : Optional[List[ServiceDescription]] #evtl. List of ServiceDescriptions
    impressum : Text
    privacy : Text
    contact : Union[ServiceDescription, Text]

class EllaContact(BaseModel):
    """
    Beispiel eines Kontakt-Formulars einer ella_app.
    """
    name : Text
    vorname : Text
    subject : Text
    message : Text
    email : Text
    telefon : Optional[Text]
    mobil : Optional[Text]

class ContactResponse(BaseModel):
    """
    Antwort an die ella_app nach Versand der Kontakt-Nachricht.
    - "success" Bool-Werte true oder false
    - "message" Exception-Message bei False, Success-Message bei  true
    """
    success : bool
    message : str
