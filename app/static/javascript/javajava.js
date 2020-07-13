// Run bellow after DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
	// Load album information when a search result is selected
	document.querySelectorAll(".listitem").forEach((a) => {
		a.addEventListener("click", () => {
			// Gather albumid stored in linklist
			var itemid = a.dataset.itemid

			// Remove search list and load album information
			document.querySelector(".resultlist").style.display = "none"
			document.querySelector("#albumrating").style.display = "inline"

			const request = new XMLHttpRequest()

			// Ajax request to server
			request.open("POST", "/album")

			// Callback function for when request completes
			request.onload = () => {
				const data = JSON.parse(request.responseText)

				// Create img tag for album art
				var picture = document.createElement("img")
				picture.src = data["images"]
				picture.style = "height:200px; width:200px;"
				document.querySelector("#albumimage").appendChild(picture)

				// Create hi tag for the album title
				var albumtitle = document.createElement("h1")
				albumtitle.innerHTML = data["name"]
				document.querySelector("#albumtitle").appendChild(albumtitle)

				// Create h3 tag for album artist
				var artist = document.createElement("h3")
				artist.innerHTML = data["artist"]
				document.querySelector("#albumartist").appendChild(artist)

				// Record length of album
				tracks = data["tracks"].length

				// Li with link for all album tracks
				for (counter = 0; counter < tracks; counter++) {
					// Add link to be albe to connect to the player
					var link = document.createElement("a")
					link.id = data["tracks"][counter]["uri"]
					link.setAttribute("data-itemid", data["tracks"][counter]["id"])
					link.className = "tracklistitem"
					link.style = "cursor: pointer;"

					// Add select tag to rate the tracks
					var select = document.createElement("select")
					select.className = "song_rating"
					select.id = data["tracks"][counter]["id"]
					select.style = "float: right;"
					select.name = "albumtracks"
					select.setAttribute("required", "")

					// Add options to the selection
					var option = document.createElement("option")
					select.appendChild(option)

					for (counter_y = 1; counter_y < 6; counter_y++) {
						var option = document.createElement("option")
						option.innerHTML = counter_y
						select.appendChild(option)
					}

					// Create list item and add data
					var list_item = document.createElement("li")
					list_item.innerHTML = data["tracks"][counter]["name"]
					list_item.appendChild(select)
					link.appendChild(list_item)
					document.querySelector("#albumtracks").appendChild(link)
				}

				// Activates the spotify player after clicking on a track
				document.querySelectorAll(".tracklistitem").forEach((a) => {
					a.addEventListener("click", () => {
						const request = new XMLHttpRequest()

						// Get song information from get_song route
						request.open("POST", "/get_song")
						request.onload = () => {
							const data = JSON.parse(request.responseText)
							document.querySelector("#songimage").src = data["image"]

							document.querySelector("#player_songname").innerHTML =
								data["name"]
							document.querySelector("#player_songartist").innerHTML =
								data["artist"]
							document.querySelector("#uri").innerHTML = data["uri"]
						}

						const data = new FormData()
						data.append("songid", a.getAttribute("data-itemid"))

						// Remove footer and add player
						document.querySelector("#sticky-footer").style.display = "none"
						document.querySelector("#web-player").style.display = "inline"

						// Add play button to player
						document.querySelector("#play").style.display = "inline"
						document.querySelector("#pause").style.display = "none"
						document.querySelector("#resume").style.display = "none"

						// Send request
						request.send(data)
					})
				})
			}

			// Add data to send with request
			const data = new FormData()
			data.append("itemid", itemid)

			// Send request
			request.send(data)
		})
	})
})
