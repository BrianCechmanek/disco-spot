import {
  initDiscordClient,
  initSpotifyClient,
  isTextChannel,
} from './providers'
// import { initSpotifyClient } from './spotify'

const PLAYLIST_ID = '74WY9gyeBKQjJVoRCWtvnj'

const dj = await initDiscordClient()
const spotify = await initSpotifyClient()

// function searchSpotify(title: string) {
//   spotify.search
// }

dj.on('ready', () => {
  console.log(`Logged in as ${dj.user?.tag}!`)
})

// dj.channels.cache.get('') as TextChannel
dj.on('messageCreate', async msg => {
  const { channel } = msg
  if (!isTextChannel(channel) || channel.name !== 'music') return
  // parse embeds
  const res = await spotify.search('Wild Wild West', { types: ['track'] })
  if (!res.tracks || res.tracks.length === 0) return
  const bestMatch = res.tracks[0]
  console.log(
    `Adding ${bestMatch.name} - ${bestMatch.artists[0].name} to playlist`
  )

  const snapshotID = await spotify.playlists.addItems(PLAYLIST_ID, [
    bestMatch.uri,
  ])
  console.log(snapshotID)
})

await dj.login(Bun.env.DISCORD_TOKEN)
// connect to server and start listening on channel

// On a message, check if it's a youtube link

// if yes, perform a basic check to see if it might be a song.
// If its a song, search the song on spotify.
// If there is no direct match, ask the user to select from a list of songs.
// automatically add the song to the playlist
//prompt user if this is correct- if yes, chill. If no, present list of search results.

function isValidYouTubeUrl(url: string): boolean {
  const regex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/
  return regex.test(url)
}
