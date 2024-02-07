import { Database } from 'bun:sqlite'
import Discord from 'discord.js'
import Spotify from 'spotify-api.js'
import type { GuildTextChannelType, TextChannel } from 'discord.js'

const db = new Database('db.sqlite', { create: true })

const needsAccessTo = Discord.GatewayIntentBits
export async function initDiscordClient() {
  const disco = new Discord.Client({
    intents: [
      needsAccessTo.Guilds,
      needsAccessTo.GuildMessages,
      needsAccessTo.MessageContent,
    ],
  })

  disco.on('messageCreate', msg => {
    if (msg.content === 'ping') {
      msg.reply('pong')
    }
  })

  return disco
}

export async function initSpotifyClient() {
  const clientID = Bun.env.SPOTIFY_ID
  const clientSecret = Bun.env.SPOTIFY_KEY

  if (!clientID || !clientSecret) {
    throw new Error('Failed to load Spotify Environment variables variables')
  }

  const client = await Spotify.Client.create({
    // refreshToken: true,
    token: {
      clientID,
      clientSecret,
    },
  })

  console.log(
    await client.auth.getUserToken({
      clientID,
      clientSecret,
      redirectURL: 'https://disco-spot.netlify.app/',
    })
  )

  return client
}

export function isTextChannel(channel: any): channel is TextChannel {
  if (!channel || typeof channel !== 'object') return false
  return channel.type === Discord.ChannelType.GuildText
}
