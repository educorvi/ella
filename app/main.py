# -*- coding: utf-8 -*-
# # Copyright (c) 2016-2020 educorvi GmbH & Co. KG
# # lars.walther@educorvi.de

from .models import Welcome, ServiceDescription, ServiceButton, FormDescription, FormData
from .models import EllaContact, ContactResponse, ResponseData, ServiceList
from .services import EllaServices
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(
    title="ELLA",
    description="OpenApi für 'Fire and Forget' Applikationen",
    version="0.9",
)
services = EllaServices()

@app.get("/")
def read_root():
    """'Ella, elle l'a' (France Gall) Die OpenApi für Deine ella_app ist online."""
    return(u"'Ella, elle l'a' (France Gall) Die OpenApi für Deine ella_app ist online.")

@app.get("/apps", response_model=ServiceList)
def get_ella_services():
    return services.get_ella_apps()

@app.get("/{ella_id}", response_model=Welcome)
def read_ella_root(ella_id:str):
    """ Liefert die Welcome-Page Deiner ella_app zurück. Das folgende Beispiel kannst Du
        ausprobieren:
        - ella_id = ella_example_simple
    """
    return services.get_welcome_page(ella_id)


@app.get("/{ella_id}/{ella_service}", response_model=ServiceDescription)
def read_ella_service(ella_id:str, ella_service:str):
     """ Liefert den gewünschten Service für Deine ella_app zurück. Folgende Beispiele kannst Du
         ausprobieren:
         - ella_id = ella_example_simple
         - ella_service:
             - ella_simple_page
             - ella_simple_service
             - ella_simple_group
     """
     return services.get_ella_service(ella_id, ella_service)


@app.post("/{ella_id}/{ella_service}/pdf", response_model=ResponseData)
def get_pdf(ella_id:str, ella_service:str, data:FormData):
    """Die ella Applikation sendet die Daten passend zu einer Servicebeschreibung. Es wird ein
       PDF-Dokument zurückgesendet.
    """
    return services.get_ellapdf(ella_id, ella_service, data)


@app.post("/{ella_id}/{ella_service}/mail", response_model=ResponseData)
def get_mail(ella_id:str, ella_service:str, data:FormData):
    """Die ella Applikation sendet die Daten passend zu einer Servicebeschreibung.
    """
    return services.get_ellamail(ella_id, ella_service, data)


@app.get("/{ella_id}/{ella_service}/docprinter/{docid}")
def get_print(ella_id:str, ella_service:str, docid:str):
    """Die ella Applikation sendet die Daten passend zu einer Servicebeschreibung.
    """
    printfile = services.get_ellaprint(ella_id, ella_service, docid)
    return FileResponse(printfile.get('filedata'), filename=printfile.get('filename'), media_type="application/pdf")


@app.post("/{ella_id}/{ella_service}/link", response_model=ResponseData)
def get_link(ella_id:str, ella_service:str, data:FormData):
    """Die ella Applikation sendet die Daten passend zu einer Servicebeschreibung.
    """
    return services.get_ellalink(ella_id, ella_service, data)


@app.post("/{ella_id}/contact/send", response_model=ContactResponse)
def get_data(ella_id:str, data:EllaContact):
    """Die ella Applikation sendet die Daten passend zum EllaContact Formular. Die Daten werden
       angenommen und weitergeleitet.
    """
    return services.send_contact_data(ella_id, data)
