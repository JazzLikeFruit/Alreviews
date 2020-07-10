var token, device

function gettoken() {
	return new Promise((resolve) => {
		const request = new XMLHttpRequest()
		request.open("POST", "/get_token")

		request.send()

		request.onload = () => {
			var data = JSON.parse(request.responseText)
			token = data["token"]
			resolve()
		}
	})
}

gettoken().then(
	(window.onSpotifyWebPlaybackSDKReady = () => {
		var player = new Spotify.Player({
			name: "Alreviews player",
			getOAuthToken: (cb) => {
				cb(token)
			},
		})
		document.querySelector("#resume_image").addEventListener("click", () => {
			player.resume().then(() => {
				document.querySelector("#pause").style.display = "inline"
				document.querySelector("#resume").style.display = "none"
				console.log("Resumed!")
			})
		})

		document.querySelector("#pause_image").addEventListener("click", () => {
			player.pause().then(() => {
				console.log("Paused!")
				document.querySelector("#resume").style.display = "inline"
				document.querySelector("#pause").style.display = "none"
			})
		})

		document.querySelector("#play_image").addEventListener("click", () => {
			play(token, document.querySelector("#uri").innerHTML, device)
			document.querySelector("#play").style.display = "none"
			document.querySelector("#pause").style.display = "inline"
		})

		// Error handling
		player.addListener("initialization_error", ({ message }) => {
			console.error(message)
		})
		player.addListener("authentication_error", ({ message }) => {
			console.error(message)
		})
		player.addListener("account_error", ({ message }) => {
			console.error(message)
		})
		player.addListener("playback_error", ({ message }) => {
			console.error(message)
		})

		// Playback status updates
		player.addListener("player_state_changed", (state) => {
			player.getCurrentState().then((state) => {
				let {
					current_track,
					next_tracks: [next_track],
				} = state.track_window

				console.log(
					"Now playing:",
					current_track["name"],
					current_track["artists"][0]["name"]
				)
			})
		})

		player.addListener("ready", ({ device_id }) => {
			console.log("Ready with Device ID", device_id)
			device = device_id
		})

		// Not Ready
		player.addListener("not_ready", ({ device_id }) => {
			console.log("Device ID has gone offline", device_id)
		})

		// Connect to the player!
		player.connect().then((success) => {
			if (success) {
				console.log("The Web Playback SDK successfully connected to Spotify!")
			}
		})
	})
)

function play(token, track, device_id) {
	let song = { uris: [track] }

	const url =
		"https://api.spotify.com/v1/me/player/play?device_id=" + device_id

	// The parameters we are gonna pass to the fetch function
	fetch(url, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
			Authorization: token[1]["Authorization"],
		},
		body: JSON.stringify(song),
	})
}
