================ ISTRUZIONI PER AVVIARE LO SCRIPT CORRETTAMENTE ================
1. Avviare QGIS Desktop
2. Dal menu superiore accedere a "Plugins >> Console python"
3. Dalla console selezionare "Mostra Editor"
4. Successivamente selezionare "Apri Script..." e selezionare lo script "StayPointDetection_.py"
5. Inserire alla fine dello script la seguente riga di codice: calculate_stay_points('C:\\..\\traj.shp', 80, 40), dove il primo parametro della funzione specifica il percorso sul proprio pc in cui è presente la traiettoria da analizzare
6. Riga 64: alla variabile "new_fn" assegnare la stringa che specifica il percorso sul proprio pc in cui lo script dovrà salvare il layer che conterrà i vari stay points individuati.
7. Selezionare "Esegui script"


================ NOTE ================
- versione di QGIS utilizzata: 3.10.0-A Coruña
- se si ha intenzione di rieseguire lo script ricordarsi, prima di rieseguirlo, di eliminare il layer "StayPoint" creato dall'algoritmo
- la colonna che rappresenta il timestamp di un determinato punto dovrà avere il seguente nome: "time"
- il formato della colonna "time" dovrà essere il seguente: YYYY/mm/dd h:m:s