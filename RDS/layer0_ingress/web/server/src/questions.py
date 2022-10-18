questions = {
    "de": {
        "Grundlegende Informationen": {
            "Was ist Sciebo RDS?": """Sciebo RDS ist ein Forschungsdatendienst, welcher sich in die Arbeitsabläufe der Forschenden integriert, indem neue Funktionen innerhalb der Hochschulcloud Sciebo ergänzt werden. Forschungsdatenmanagement und wissenschaftliche Analysen auf Basis von Forschungsdaten werden damit noch einfacher und reibungsloser.
Für Sciebo RDS benötigen Sie kein neues Nutzerkonto, Sie können hierfür Ihr bereits vorhandenes Sciebo-Konto nutzen. Für die zu verknüpfenden Dienste können Sie ebenfalls Ihre bereits bestehenden Konten nutzen, soweit vorhanden.
Aktuell verknüpft Sciebo RDS verschiedene Dienste, um Ihre Daten aus der Hochschulcloud heraus zu publizieren oder zu archivieren. Weitere Informationen dazu finden Sie auf der [offiziellen Webseite](https://www.research-data-services.org/)."""
        },
        "Daten veröffentlichen": {
            "Wie kann ich Daten veröffentlichen?": """Über Sciebo RDS können Sie Daten bei Zenodo veröffentlichen. Prinzipiell können alle Arten von (Forschungs-)Daten und Datenformaten durch Sciebo RDS veröffentlicht werden. Im Sinne einer guten Nachnutzbarkeit der Daten durch Dritte ist es allerdings empfehlenswert, bei der Übermittlung der Daten an einen Dienst keine binären oder proprietären Formate zu wählen, sondern solche, die frei verfügbar sind. Achten Sie außerdem darauf, dass eine gewisse Größe der Daten nicht überschritten wird. Bei Zenodo gibt es bspw. eine Obergrenze von 50 GB pro Datensatz.
Um Daten zu veröffentlichen, müssen Sie ein Projekt anlegen. Vor der Veröffentlichung können Sie sämtliche Daten (Forschungsdaten/ Metadaten etc.) des Projekts ändern. Sobald Ihre Daten veröffentlicht wurden, ist das Projekt in Sciebo RDS nicht mehr bearbeitbar. Falls Sie nachträglich Metadaten korrigieren wollen, müssen Sie dies innerhalb des gewählten Diensts tun. Falls Daten erneut veröffentlicht werden sollen, muss dafür ein neues Projekt angelegt werden. Dieses Vorgehen gewährleistet, dass Daten immer mit einer einzigartigen Identifikationsnummer (kurz DOI) versehen werden können. """,
            "Projekte anlegen": """Um ein Projekt anzulegen, klicken Sie links im Menü auf den Reiter „Projekte“. Im darauffolgenden Fenster können Sie mit Klick auf das grüne Plus-Symbol unter rechts ein neues Projekt erzeugen. Im nächsten Schritt sollten Sie das Projekt konfigurieren. Klicken Sie dazu auf das gewünschte Projekt und geben Sie alle benötigten Informationen an: 
            
1. Ordner, der die zu übermittelnden Daten beinhaltet, 
2. Dienste, die die Daten erhalten sollen. (Sollten hier keine Dienste auswählbar sein, müssen Sie diese zuerst unter dem Reiter *Dienste* aktivieren.) Sobald alle Informationen hinterlegt wurden, können Sie mit *Weiter* bestätigen und die Metadaten des Projektes eintragen. 
3. Abschließend können Sie Ihre Angaben noch einmal einsehen und überprüfen.

Sollten Sie mit Ihren Angaben zufrieden sein, können Sie nun die Daten übermitteln.""",
            "Dienste aktivieren / deaktivieren": """Um einen Dienst hinzuzufügen, gehen Sie bitte im linken Menü auf den Reiter „Dienste“. Sie erhalten dann eine Übersicht aller verfügbaren Dienste, aus denen Sie den gewünschten auswählen können. Mit Klick auf den Dienst klappt darunter ein Konfigurationsfenster auf. Klicken Sie auf „verbinden“. In einem neuen Browser-Tab werden Sie anschließend aufgefordert, sich bei dem entsprechenden Dienst anzumelden oder zu registrieren, sollten Sie dafür noch keine Zugangsdaten haben. In der Regel schließt sich der neu geöffnete Tab von alleine wieder und leitet Sie zurück zu Sciebo RDS. Sollte dies nicht der Fall sein, schließen Sie den Tab bitte händisch, gehen zu Sciebo RDS zurück und überprüfen Sie, ob die Aktivierung des Dienstes erfolgreich gekappt hat. Sollten bei einem zweiten Aktivierungsversuch immer noch Probleme auftreten, wenden Sie sich bitte an $SUPPORT_EMAIL}.
Um einen Dienst in Sciebo RDS zu deaktivieren, klicken Sie bei dem entsprechenden Dienst auf „trennen“. Sciebo RDS wird den Zugriff dann sperren. Sämtliche Daten, die durch das Zugriffsrecht an den Dienst übermittelt wurden, sind davon unberührt. """,
        },
        "Metadaten verwalten": {
            "Wie kann ich meine Metadaten verwalten?": """Metadaten können in Sciebo RDS innerhalb eines Projektes verwaltet und bearbeitet werden. Vor dem Abschluss eines Projekts und der Übermittlung der Daten an einen Dienst können Sie sämtliche Daten des Projekts (Forschungsdaten/Metadaten etc.) ändern. Sobald Ihre Daten übermittelt wurden, ist das Projekt und damit auch die (Meta-)Daten in Sciebo RDS nicht mehr bearbeitbar. Dieses Vorgehen gewährleistet, dass Daten immer mit einer einzigartigen Identifikationsnummer (kurz DOI) versehen werden können. Einige Dienste (wie Zenodo) lassen eine nachträgliche Aktualisierung von (Meta-)Daten durch das Vergeben einer verwandten DOI zu. Sciebo RDS unterstützt dies aber zum aktuellen Zeitpunkt noch nicht. Falls Sie nachträglich (Meta-)Daten korrigieren wollen, müssen Sie dies daher innerhalb des gewählten Diensts tun, sofern möglich. Alternativ können Sie in Sciebo RDS ein neues Projekt mit den korrekten Daten anlegen und diese erneut übermitteln.""",
        },
        "Konto verwalten": {
            "Wie funktioniert die Diensteverwaltung?": "Sciebo RDS nutzt die Oauth2-Technologie. Hierbei werden im Namen des:der Nutzer:in Informationen mit Diensten ausgetauscht, ohne dabei Passwörter oder andere kritische Daten zu übermitteln. Ist die Dienstleistung durch Sciebo RDS nicht mehr erwünscht, können die Zugriffsrechte ohne Weiteres durch den:die Nutzer:in wieder entzogen werden. Für die Arbeit mit Sciebo RDS ist es nicht notwendig, alle angebotenen Dienste zu aktivieren. Sie können später jederzeit weitere Dienste hinzufügen oder nicht mehr genutzte Dienste entfernen.",
            "Dienste aktivieren / deaktivieren": """Um einen Dienst hinzuzufügen, gehen Sie bitte im linken Menü auf den Reiter „Dienste“. Sie erhalten dann eine Übersicht aller verfügbaren Dienste, aus denen Sie den gewünschten auswählen können. Mit Klick auf den Dienst klappt darunter ein Konfigurationsfenster auf. Klicken Sie auf „verbinden“. In einem neuen Browser-Tab werden Sie anschließend aufgefordert, sich bei dem entsprechenden Dienst anzumelden oder zu registrieren, sollten Sie dafür noch keine Zugangsdaten haben. In der Regel schließt sich der neu geöffnete Tab von alleine wieder und leitet Sie zurück zu Sciebo RDS. Sollte dies nicht der Fall sein, schließen Sie den Tab bitte händisch, gehen zu Sciebo RDS zurück und überprüfen Sie, ob die Aktivierung des Dienstes erfolgreich gekappt hat. Sollten bei einem zweiten Aktivierungsversuch immer noch Probleme auftreten, wenden Sie sich bitte an $SUPPORT_EMAIL.
Um einen Dienst in Sciebo RDS zu deaktivieren, klicken Sie bei dem entsprechenden Dienst auf „trennen“. Sciebo RDS wird den Zugriff dann sperren. Sämtliche Daten, die durch das Zugriffsrecht an den Dienst übermittelt wurden, sind davon unberührt. """,
            "Konto verwalten / löschen": """Bei der ersten Verwendung von Sciebo RDS wird automatisch ein persönliches Sciebo-RDS-Konto angelegt. Für die einfache Handhabung wird der Kontozugang über die Hochschulcloud Sciebo gesteuert. Das bedeutet, solange Ihr Sciebo-Account aktiv ist, bleibt auch Sciebo RDS aktiv, sofern Sie Sciebo RDS nicht händisch deaktivieren.

Möchten Sie Sciebo RDS im Gesamten deaktivieren bzw. Ihr Sciebo-RDS-Nutzerkonto löschen, gehen Sie unten links auf „Einstellungen“ und anschließend auf „RDS löschen“. Sämtliche Daten, die Sie in Sciebo RDS hinterlegt haben, werden damit unwiederbringlich gelöscht. Daten, die Sie über Sciebo RDS an andere Dienste übermittelt haben und die nun bei diesen Diensten liegen, sind davon unberührt. Ihre Daten in der Hochschulcloud Sciebo sind davon ebenfalls unberührt und werden durch Deaktivieren von Sciebo RDS *nicht* gelöscht."""
        },
    },
    "en": {
        "General Information": {
            "What is Sciebo RDS?":
                """Sciebo RDS is a research data service that integrates into researchers' workflows by adding new functionality within a research cloud. Research data management and scientific analyses based on research data thus become even easier and smoother.
Currently, Sciebo RDS allows you to link various repositories to publish or archive your research data. You don't need a new user account to use Sciebo RDS, you can use your existing Sciebo account. If you have one, you can link your existing repository account to Sciebo RDS.

Visit the *Repositories* tab to see what repositories available.
If you are having trouble using Sciebo RDS or have further questions, please contact $SUPPORT_EMAIL.

Sciebo RDS is developed by the [University of Münster](https://www.uni-muenster.de/), Germany. Further information on the project is available on the [official website](https://www.research-data-services.org/)."""
        },
        "Publishing Data": {
            "How can I connect/disconnect repositories?": """To add a repository, go to the *Repositories* tab. You will see an overview of all available repositories. Click *Connect* to connect to a repository. A new browser tab will open and you will be prompted to log in to the corresponding repository or to register if you do not yet have an account. Usually the newly opened tab will close by itself and redirect you back to Sciebo RDS. If this is not the case, please close the tab manually, go back to Sciebo RDS and check if the repository connected successfully. If you encounter problems, please contact $SUPPORT_EMAIL.

To disconnect a repository from Sciebo RDS, click "disconnect" on the corresponding repository. All data previously published to the repository will stay unaffected.""",
            "How can I publish data? How does the Project Workflow work?": """You can publish data using the **Project Workflow**.

Click the *Projects* tab in the menu on the left. You can now create a new project by clicking the `New Project` button. A new project will be created, which you now have to configure to your needs - you will be asked to:
                
1. select a folder on your Sciebo account, that contains the data to be published/archived,
2. name your project (this name will only be used to help you identify the project within RDS),
3. select the repository that will receive the data (you need at least one repository connected in *Repositories* tab for this).      

<br/>

Click *Continue* and use the embedded metadata editor to enrich your project with metadata. Next, click *Continue* again. Confirm that you have set the correct project folder and repository and click *Publish* to submit you data.

The *Configuration*, *Metadata* and *Publish* step of the workflow may be done at different times. The configuration will be saved as soon as you click *Continue*, the metadata will be saved as soon as it is submitted to the interface.  
 Each project can only be published to *one* repository. But you can have multiple projects with the same folder and different repositories selected. Once your data is published, the project is no longer editable in Sciebo RDS. If you want to correct metadata afterwards, you must do so within the selected repository. If data is to be published again, a new project must be created for this purpose. This procedure ensures that data can always be assigned a unique identification number (DOI for short).""",
            "What kind of data can be published through Sciebo RDS?" : """In principle, all kinds of (research) data and data formats can be published. However, in order to ensure good reusability of the data by third parties, it is recommended not to choose binary or proprietary formats when submitting data to a repository, but to choose formats that are freely available. Also, make sure that a certain size of data is not exceeded. Zenodo, for example, has an upper limit of 50 GB per data set.""",
        },
        "Managing Metadata": {
            "How can I manage metadata?":
                """The second step of the **Project Workflow** will provide you with an metadata editor to add and modify metadata. Once your data has been submitted, the project and therefore the (meta)data is no longer editable in Sciebo RDS. This procedure ensures that data can always be assigned a unique identification number (DOI for short).    
                    Some repositories (like Zenodo) allow a subsequent update of (meta)data by assigning a related DOI. However, this has to be done within the Zenodo interface, it is not possible within Sciebo RDS. Alternatively, you can create a new project in Sciebo RDS with the correct data and resubmit. """
        },
        "Account Management": {
            "How does the account management work?": """Sciebo RDS uses the Oauth2 technology. This means that information is exchanged with repositories without actually transmitting passwords or other critical data to Sciebo RDS. If the service provided by Sciebo RDS is no longer desired, access rights can easily be revoked by the user.

You can always add more or remove repositories in the Sciebo RDS *Repositories* tab.""",
        },
    }
}
