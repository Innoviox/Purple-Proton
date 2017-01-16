# Purple-Proton

A basic static move generator using the STAX algorithm.

#Steps:

* Generate words: GAC
    * Using `itertools.permutations`
    * Repeating for each word length 2...7
* Generate possible places to play (not through a letter): STARMAP
    * Places next to each letter
    * This is the step that needs the most optimization
* Check if you can play in each play for each word for each direction
    * The directions are across and down
    * This part should be optimized too
* Then use SLOTIFY to get the rest done
    * Go through each row & column, called a "slot"
    * Turn all of the special tiles into empty spaces, represented by `'.'`
    * Using the GAC again, but this time without the "valid word" filter
    * Put all GAC-ed combinations infront of every letter
    * Check
An example STAX session might look like this, with starting rack `'ASW'` and starting board "BAG" at (8, 7):

  ---------------------------------------------------------------
  |  | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
  ----------------------------------------------------------------
  |01|TWS|   |   |DLS|   |   |   |TWS|   |   |   |DLS|   |   |TWS|
  ----------------------------------------------------------------
  |02|   |DWS|   |   |   |TLS|   |   |   |TLS|   |   |   |DWS|   |
  ----------------------------------------------------------------
  |03|   |   |DWS|   |   |   |DLS|   |DLS|   |   |   |DWS|   |   |
  ----------------------------------------------------------------
  |04|DLS|   |   |DWS|   |   |   |DLS|   |   |   |DWS|   |   |DLS|
  ----------------------------------------------------------------
  |05|   |   |   |   |DWS|   |   |   |   |   |DWS|   |   |   |   |
  ----------------------------------------------------------------
  |06|   |TLS|   |   |   |TLS|   |   |   |   |   |   |   |TLS|   |
  ----------------------------------------------------------------
  |07|   |   |DLS|   |   |   |DLS|   |DLS|   |   |   |DLS|   |   |
  ----------------------------------------------------------------
  |08|TWS|   |   |DLS|   |   | B | A | G |   |   |DLS|   |   |TWS|
  ----------------------------------------------------------------
  |09|   |   |DLS|   |   |   |DLS|   |DLS|   |   |   |DLS|   |   |
  ----------------------------------------------------------------
  |10|   |TLS|   |   |   |TLS|   |   |   |TLS|   |   |   |TLS|   |
  ----------------------------------------------------------------
  |11|   |   |   |   |DWS|   |   |   |   |   |DWS|   |   |   |   |
  ----------------------------------------------------------------
  |12|DLS|   |   |DWS|   |   |   |   |   |   |   |DWS|   |   |DLS|
  ----------------------------------------------------------------
  |13|   |   |DWS|   |   |   |DLS|   |DLS|   |   |   |DWS|   |   |
  ----------------------------------------------------------------
  |14|   |DWS|   |   |   |TLS|   |   |   |TLS|   |   |   |DWS|   |
  ----------------------------------------------------------------
  |15|TWS|   |   |DLS|   |   |   |TWS|   |   |   |DLS|   |   |TWS|
  ----------------------------------------------------------------

  AW (9, 7) done 1
  AW (7, 7) done 1
  AW (8, 8) done 1
  AW (8, 6) done 1
  AW (9, 8) done 2
  AW (7, 8) done 3
  AW (8, 9) done 3
  AW (8, 7) done 3
  AW (9, 9) done 3
  AW (7, 9) done 4
  AW (8, 10) done 4
  SAW (9, 7) done 4
  SAW (7, 7) done 4
  SAW (8, 8) done 4
  SAW (8, 6) done 4
  SAW (9, 8) done 5
  SAW (7, 8) done 5
  SAW (8, 9) done 5
  SAW (8, 7) done 5
  SAW (9, 9) done 5
  SAW (7, 9) done 5
  SAW (8, 10) done 6
  WAS (9, 7) done 6
  WAS (7, 7) done 6
  WAS (8, 8) done 6
  WAS (8, 6) done 6
  WAS (9, 8) done 7
  WAS (7, 8) done 7
  WAS (8, 9) done 7
  WAS (8, 7) done 7
  WAS (9, 9) done 7
  WAS (7, 9) done 7
  WAS (8, 10) done 8
  ...............
  ...............
  ...............
  ...............
  ...............
  ...............
  ...............
  ......BAG......
  .....ABAG......
  ......BAGA.....
  .....SBAG......
  ......BAGS.....
  .....WBAG......
  ......BAGW.....
  ....ASBAG......
  .....ABAGS.....
  ......BAGAS....
  ....AWBAG......
  .....ABAGW.....
  ......BAGAW....
  ....SABAG......
  .....SBAGA.....
  ......BAGSA....
  ....SWBAG......
  .....SBAGW.....
  ......BAGSW....
  ....WABAG......
  .....WBAGA.....
  ......BAGWA....
  ....WSBAG......
  .....WBAGS.....
  ......BAGWS....
  ...ASWBAG......
  ....ASBAGW.....
  .....ABAGSW....
  ......BAGASW...
  ...AWSBAG......
  ....AWBAGS.....
  .....ABAGWS....
  ......BAGAWS...
  ...SAWBAG......
  ....SABAGW.....
  .....SBAGAW....
  ......BAGSAW...
  ...SWABAG......
  ....SWBAGA.....
  .....SBAGWA....
  ......BAGSWA...
  ...WASBAG......
  ....WABAGS.....
  .....WBAGAS....
  ......BAGWAS...
  ...WSABAG......
  ....WSBAGA.....
  .....WBAGSA....
  ......BAGWSA...
  ...............
  ...............
  ...............
  ...............
  ...............
  ...............
  ...............
  .........1..2...
  ...............
  ...............
  ...............
  ...............
  ...............
  ...............
  .......B.......
  ......AB.......
  .......BA......
  ......SB.......
  .......BS......
  ......WB.......
  .......BW......
  .....ASB.......
  ......ABS......
  .......BAS.....
  .....AWB.......
  ......ABW......
  .......BAW.....
  .....SAB.......
  ......SBA......
  .......BSA.....
  .....SWB.......
  ......SBW......
  .......BSW.....
  .....WAB.......
  ......WBA......
  .......BWA.....
  .....WSB.......
  ......WBS......
  .......BWS.....
  ....ASWB.......
  .....ASBW......
  ......ABSW.....
  .......BASW....
  ....AWSB.......
  .....AWBS......
  ......ABWS.....
  .......BAWS....
  ....SAWB.......
  .....SABW......
  ......SBAW.....
  .......BSAW....
  ....SWAB.......
  .....SWBA......
  ......SBWA.....
  .......BSWA....
  ....WASB.......
  .....WABS......
  ......WBAS.....
  .......BWAS....
  ....WSAB.......
  .....WSBA......
  ......WBSA.....
  .......BWSA....
  .......A.......
  ......AA.......
  .......AA......
  ......SA.......
  .......AS......
  ......WA.......
  .......AW......
  .....ASA.......
  ......AAS......
  .......AAS.....
  .....AWA.......
  ......AAW......
  .......AAW.....
  .....SAA.......
  ......SAA......
  .......ASA.....
  .....SWA.......
  ......SAW......
  .......ASW.....
  .....WAA.......
  ......WAA......
  .......AWA.....
  .....WSA.......
  ......WAS......
  .......AWS.....
  ....ASWA.......
  .....ASAW......
  ......AASW.....
  .......AASW....
  ....AWSA.......
  .....AWAS......
  ......AAWS.....
  .......AAWS....
  ....SAWA.......
  .....SAAW......
  ......SAAW.....
  .......ASAW....
  ....SWAA.......
  .....SWAA......
  ......SAWA.....
  .......ASWA....
  ....WASA.......
  .....WAAS......
  ......WAAS.....
  .......AWAS....
  ....WSAA.......
  .....WSAA......
  ......WASA.....
  .......AWSA....
  .......G.......
  ......AG.......
  .......GA......
  ......SG.......
  .......GS......
  ......WG.......
  .......GW......
  .....ASG.......
  ......AGS......
  .......GAS.....
  .....AWG.......
  ......AGW......
  .......GAW.....
  .....SAG.......
  ......SGA......
  .......GSA.....
  .....SWG.......
  ......SGW......
  .......GSW.....
  .....WAG.......
  ......WGA......
  .......GWA.....
  .....WSG.......
  ......WGS......
  .......GWS.....
  ....ASWG.......
  .....ASGW......
  ......AGSW.....
  .......GASW....
  ....AWSG.......
  .....AWGS......
  ......AGWS.....
  .......GAWS....
  ....SAWG.......
  .....SAGW......
  ......SGAW.....
  .......GSAW....
  ....SWAG.......
  .....SWGA......
  ......SGWA.....
  .......GSWA....
  ....WASG.......
  .....WAGS......
  ......WGAS.....
  .......GWAS....
  ....WSAG.......
  .....WSGA......
  ......WGSA.....
  .......GWSA....
  ...............
  ...............
  ...............
  ...............
  ...............
  ...............