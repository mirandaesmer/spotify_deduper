# spotify_deduper
Spotify Playlist Bulk De-duplicator. Created for quickly identifying duplicate
songs in large spotify libraries. Also useful for organizing large libraries 
into a pre-defined structure (defined below). Initially developed for personal
use. *NOTE: These scripts avoid any write operations in order to ensure no 
overwriting or bugs caused by API changes.*

### Definitions
- PLAYLIST: a set of 50 unique songs with a descriptive label and description.
- GENRE: Predefined groupings for playlists, used for deduplicating between
similar playlists or defining playlists to exclude.
*NOTE: created before spotify added folder functionality to libraries, 
folders are a viable alternative, but my personal library is too large to 
update to use folders.*


### Labels
- Playlist names are split into 4 parts, 2 in the spotify playlist name and 
in the spotify playlist description. 
    - NAME - MUSIC DESCRIPTION
    - GENRE - OTHER DETAILS
- Labels in the name are used to identify how many songs are in the playlist. 
    - UPPERCASE - playlist has exactly 50 songs with no duplicates.
    - Capitalized - playlist has less than 50 songs and may have duplicates.
    - lowercase - playlist is very new or has less than 25 songs.

### TODO
- Add ability to track which playlists are public and which are private.
- Add tests for SpotipyDeduper.get_badly_labeled_playlists()
- Add docstring for SpotipyDeduper.get_badly_labeled_playlists()
- Add docstring for SpotipyWrapper.get_all_liked_songs(), NOTE: function is 
currently time-costly.
- 