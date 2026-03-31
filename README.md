# Accordi-to-Pdf
Questa repository contiene codice e istruzioni per produrre file pdf con gli accordi del sito Accordi e Spartiti

### Premesse
Tutti i diritti su canzoni e accordi sono dei rispettivi proprietari. Questa applicazione ispeziona la pagina HTML di uno specificato url e ne estrae le informazioni, in accordo col fair use. Usare solo per scopi didattici e personali.

### Utilizzo
L'applicazione è scritta in Python e ha alcune dipendenze:

!pip install pypdf re os markdown_pdf

Una volta completato il setup è possibile estrarre gli accordi desiderati mettendo nella stessa directory del programma un file "canzoni.txt" contenente gli **url** di tutte le canzoni desiderate dal sito **accordi e spartiti**. Il programma estrarrà gli accordi e il testo e produrrà un pdf per ciascuna canzone, infine unirà i pdf in un unico pdf file ordinato alfabeticamente per nome artista. 

Qualora si desideri scaricare una canzone con accordi trasposti, inserire il valore su "trasposizione" (es +1 -> inserire 1).

## Future development
Alcuni possibili sviluppi futuri:
1) Miglioramento della grafica dei pdf, su due colonne per pagina
2) Evidenziazione in grassetto degli accordi
3) Estensione ad altri siti come Ultimate Guitar

Ogni contribuzione è ben accetta :) enjoy!
