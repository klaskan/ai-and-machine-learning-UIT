# TODO

## Fakta

- Graf algoritme på lik linje som Dijkstra. 
- A* finner korteste veide vei fra et punkt til et annet punkt, og har ikke det samme behovet som Dijkstra å gå gjennom hele grafen. 
- A* tar i bruk dynamisk programmering og heuristikk
- Når du skal lage A* kan du ta i bruk mye av Dijkstra siden der er veldig like!

## A* algoritmen

- Den mest sentrale ligningen i algoritmen er: F(n) = G(n) + H(n)
- n = noden
- G(n) representerer kostnaden fra start-noden og frem til noden n
- F(n) er totalkostnden i noden n
- H(n) er den heuristiske verdien i n 
- Så det hele funksjonen F(n) = G(n) + H(n) forteller oss er at for en node n så er det sånn at den har en målt avstand G(n) som er den avstanden fra startnoden
    som man skal bevege seg fra og frem til den noden man står nå, dette er den korsteste veide veien fra startnoden til den aktuelle noden man står i. Og så har
    man en heuristisk funksjon H(n) som beregner manhattan avstanden fra den noden man står i n frem til dit man skal (aka destinasjonen). F(n) er totalkostnaden av
    disse to.
- H(n) tar i bruk en heuristiske funksjon som gjør denne algoritmen mye mer målrettet. I heuristiske funksjonen tar inn en start node og en target node. Så tar vi 
    nodene etter hvert som vi traverserer gjennom a* og deler dem opp i to forskjellige deler: ubehandlede noder og ferdigbehandlede noder. 
    En ubehandlet node kan være under behandling, men den må i hvert fall behandles. Ferdigbehandlede noder trenger vi ikke å besøke flere ganger. 
- Man starter A* på følgende måte: 1. tar noden som utgjør startnoden og dytter den inn på openset som er en prioritetskø. Startnoden får da en G som er avstanden fra 
    startnoden til nåværende node som da blir 0. Den heuristiske verdien er det funksjonen sier at den skal være, fra starnoden til sluttnoden, og verdien av H og G puttes
    i F. Prioritetskøen er prioritet på F, ikke på G eller H. 


## A* Pseudo-Kode

current - Noden som behandles nå
targetNode - sluttnoden
edge - Kanten ut fra en node, kant består av en "weight" og en "node" som kanten går til

while openSet is not empty  #Så lenge vi har ubehandlede noder  
    current = get node from openSet while removing the (current) node from openSet #så skal man hente ut den første noden i openSet 
    if current = targetNode #Dersom dette er target noden break
        break
    add current to closedSet    #Dersom ikke target node, legg til i closedSet med behandlede noder.
    for every edge in current.adjecent  #For hver gang man finner en kant i adjecent listen til den den nåværende noden, gå inn og se om den noden man finnee i kanten er:
        if edge.node not marked for updates before (not in openSet) #Går inn og ser om noden som man finner i denne kanten om den er markert for oppdateringer før(finnes den i openSet?)
            if edge.node not already updated before (not in closed set) #Dersom den heller ikke finnes i closed, da setter du:
                edge.node.previous = current # Da setter man previous til å være current node
                edge.node.g = current.g + edge.weight # Setter nodens korteste veide vei til å være current.g + edge.weight
                edge.node.h = heuristic(edge.node, targetnode) #Setter heuristilken funksjonen til å våre en funksjon av den aktuelle noden til target noden
                edge.node.f = edge.node.g + edge.node.f #Selv forklarende
                add the edge.node to openSet #Putter så edge.noden inn på openSet, siden den ikke var på openSet eller closedSet
            else #Dersom 
                if edge.node.g > current.g + edge.weight
                    edge.node.previous = current
                    edge.node.g = current.g  




