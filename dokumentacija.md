# Analiza i implementacija protokola linearnog konsenzusa u multi-agentnim sistemima

**Apstrakt**
Ovaj projekat istražuje implementaciju i simulaciju algoritama konsenzusa u umreženim multi-agentnim sistemima. Konkretno, analiziramo standardni protokol linearnog konsenzusa i poredimo ga sa Max-Consensus strategijom. Sistem je implementiran koristeći MESA okvir u Python-u, pridržavajući se principa čiste arhitekture kako bi se osigurala modularnost i proširivost. Rezultati simulacije pokazuju svojstva konvergencije oba protokola pod različitim topologijama mreže.

## 1. Uvod
U oblasti distribuiranog upravljanja i multi-agentnih sistema (MAS), problemi konsenzusa — gde grupa agenata mora da se usaglasi oko zajedničke vrednosti — su fundamentalni. Primene se kreću od kontrole formacije bespilotnih letelica do distribuiranih senzorskih mreža. Kao što su diskutovali Olfati-Saber i saradnici u *Consensus and Cooperation in Networked Multi-Agent Systems*, algoritmi koji omogućavaju brzo usaglašavanje su ključni za efikasan timski rad.

Ovaj projekat ima za cilj simulaciju ovih dinamika, omogućavajući agentima sa nesavršenim lokalnim merenjima da komuniciraju sa susedima i konvergiraju ka zajedničkom stanju.

## 2. Metodologija

### 2.1 Protokol linearnog konsenzusa
Primarni implementirani protokol je algoritam linearnog konsenzusa u diskretnom vremenu. Za agenta $i$ sa stanjem $x_i$ u vremenu $k$, pravilo ažuriranja je dato sa:

$$ x_i(k+1) = x_i(k) + \epsilon \sum_{j \in N_i} (x_j(k) - x_i(k)) $$

Gde je:
- $N_i$ skup suseda agenta $i$.
- $\epsilon$ veličina koraka (0 < $\epsilon$ < $1/\Delta_{max}$).
- Sistem konvergira ka proseku početnih stanja: $\bar{x} = \frac{1}{N} \sum x_i(0)$.

### 2.2 Max-Consensus Protokol
Kao alternativu za poređenje, implementirali smo Max-Consensus protokol. Ovo je nelinearna strategija koja se često koristi za izbor lidera ili pronalaženje ekstrema. Pravilo ažuriranja je:

$$ x_i(k+1) = \max(x_i(k), \max_{j \in N_i} x_j(k)) $$

Agenti jednostavno usvajaju najveću vrednost primećenu u njihovom lokalnom susedstvu. Sistem konvergira ka globalnom maksimumu početnih stanja.

### 2.3 Mrežne topologije i njihov uticaj
Topologija mreže diktira kako informacije teku između agenata, direktno utičući na **brzinu konvergencije** (koliko brzo se usaglašavaju). Ovaj projekat implementira tri različite topologije:

1.  **Slučajni graf (Erdős-Rényi)**
    -   **Struktura**: Agenti su povezani nasumično sa verovatnoćom $p$ (podrazumevano 0.3).
    -   **Uticaj**: Ovo modeluje realistične ad-hoc mreže. Brzina konvergencije je generalno brza, određena "algebarskom povezanošću" (druga najmanja sopstvena vrednost Laplasove matrice). Sve dok je graf povezan, agenti će relativno brzo postići konsenzus.

2.  **Prstenasta rešetka (Ring Lattice)**
    -   **Struktura**: Agenti su raspoređeni u krug, povezani samo sa svojim neposrednim levim i desnim susedima.
    -   **Uticaj**: Ova topologija ima veliki **dijametar** (udaljenost između najudaljenijih čvorova). Informacije putuju sporo, skok-po-skok. Posledično, konvergencija je **veoma spora**, posebno za linearni konsenzus, jer se vrednosti postepeno difuzuju kroz prsten.

3.  **Potpuno povezan (Fully Connected)**
    -   **Struktura**: Svaki agent je povezan sa svakim drugim agentom.
    -   **Uticaj**: Dijametar je 1.
        -   Za **Max-Consensus**, konvergencija je trenutna (1 korak), jer svaki agent odmah vidi globalni maksimum.
        -   Za **Linearni konsenzus**, konvergencija je izuzetno brza jer se "mešanje" vrednosti dešava globalno u svakoj iteraciji.

## 3. Arhitektura sistema
Softver je projektovan prateći principe **Čiste arhitekture** i **Objektno-orijentisanog programiranja (OOP)** kako bi se osiguralo razdvajanje odgovornosti.

### 3.1 Slojeviti dizajn
- **Domain Layer (Sloj domena)**: Definiše apstraktne bazne klase (`AbstractSimulation`, `AbstractProtocol`) koje predstavljaju osnovnu poslovnu logiku nezavisnu od detalja implementacije.
- **Models Layer (Sloj modela)**: Koristi **Pydantic** za rigoroznu validaciju podataka konfiguracije i stanja agenata.
- **Simulation Layer (Sloj simulacije)**: Izgrađen na **MESA** okviru. `ConsensusAgent` i `ConsensusModel` upravljaju logikom modelovanja zasnovanog na agentima.
- **Protocols Layer (Sloj protokola)**: Implementira **Strategy Pattern** (obrazac strategije) putem `ProtocolFactory`, omogućavajući dinamičku promenu algoritama konsenzusa bez izmene koda agenata.
- **Services Layer (Sloj servisa)**: **Singleton** servisi za Konfiguraciju i Logovanje osiguravaju konzistentno upravljanje globalnim stanjem.
- **UI Layer (Sloj korisničkog interfejsa)**: GUI zasnovan na **Tkinter**-u pruža vizuelizaciju stanja agenata u realnom vremenu.

### 3.2 MESA Okvir
MESA je modularni okvir za izgradnju, analizu i vizuelizaciju modela zasnovanih na agentima u Python-u. Omogućava korisnicima da kreiraju modele koristeći ugrađene osnovne komponente (kao što su prostorne mreže i planeri agenata) ili prilagođene implementacije. U ovom projektu, MESA pruža osnovu za simulaciju:
- **Model Class**: Upravlja globalnim stanjem, vremenskim koracima i okruženjem (topologija grafa).
- **Agent Class**: Bazna klasa za `ConsensusAgent`, koja upravlja jedinstvenim ID-ovima i referencama modela.
- **NetworkGrid**: Upravlja topološkim vezama između agenata, omogućavajući efikasne upite suseda neophodne za protokole konsenzusa.
- **Data Collection**: (Implicitno korišćeno) MESA olakšava praćenje stanja agenata tokom vremena, koje ručno agregiramo za GUI i grafikone verifikacije.

## 4. Detalji implementacije
Projekat je razvijen u Python-u 3.12. 

- **Logika agenta**: Svaki `ConsensusAgent` održava lokalno stanje i referencu na strategiju protokola. U svakom koraku, on ispituje svoje susede putem MESA mreže i primenjuje pravilo ažuriranja protokola.
- **Rukovanje šumom**: Da bi se simulirali senzori iz stvarnog sveta, Gausov šum se može ubaciti u ažuriranja linearnog konsenzusa, omogućavajući analizu robusnosti protokola.

## 5. Rezultati i diskusija
Simulacije su sprovedene sa $N=10$ do $N=100$ agenata.

- **Linearni konsenzus**: Agenti su uspešno konvergirali ka prosečnoj vrednosti. Vreme konvergencije se povećavalo sa retkošću grafa (npr. prstenasta topologija je trajala znatno duže od slučajnog grafa).
- **Max-Consensus**: Konvergencija je bila izuzetno brza, propagirajući maksimalnu vrednost kroz dijametar mreže u $D$ koraka, gde je $D$ dijametar grafa.

Poređenje naglašava kompromis između tipa dogovora (prosek naspram ekstrema) i brzine konvergencije.

## 6. Zaključak
Uspešno smo implementirali modularno simulaciono okruženje za protokole konsenzusa. Upotreba dizajnerskih obrazaca kao što su Factory i Strategy omogućila je besprekorno poređenje različitih algoritama. Rezultati potvrđuju teorijska svojstva konvergencije protokola linearnog i Max-Consensus-a. Budući rad bi mogao proširiti ovaj okvir tako da uključi dinamiku lider-pratilac ili promenljive topologije.

## Reference
1. R. Olfati-Saber, J. A. Fax and R. M. Murray, "Consensus and Cooperation in Networked Multi-Agent Systems," in *Proceedings of the IEEE*, vol. 95, no. 1, pp. 215-233, Jan. 2007.
