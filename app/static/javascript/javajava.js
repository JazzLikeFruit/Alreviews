document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".listitem").forEach((a) => {
		a.addEventListener("click", () => {
			var itemid = a.dataset.itemid
			document.querySelector(".resultlist").style.display = "none"
			document.querySelector("#albumrating").style.display = "inline"
			const request = new XMLHttpRequest()

			request.open("POST", "/album")

			// Callback function for when request completes
			request.onload = () => {
				const data = JSON.parse(request.responseText)

				var picture = document.createElement("img")
				picture.src = data["images"]
				picture.style = "height:200px; width:200px;"
				document.querySelector("#albumimage").appendChild(picture)

				var albumtitle = document.createElement("h1")
				albumtitle.innerHTML = data["name"]
				document.querySelector("#albumtitle").appendChild(albumtitle)

				var artist = document.createElement("h3")
				artist.innerHTML = data["artist"]
				document.querySelector("#albumartist").appendChild(artist)
				tracks = data["tracks"].length
				for (i = 0; i < tracks; i++) {
					var link = document.createElement("a")
					link.id = data["tracks"][i]["uri"]
					link.setAttribute("data-itemid", data["tracks"][i]["id"])
					link.className = "tracklistitem"
					link.style = "cursor: pointer;"

					var select = document.createElement("select")
					select.className = "song_rating"
					select.id = data["tracks"][i]["id"]
					select.style = "float: right;"

					var option = document.createElement("option")
					select.appendChild(option)

					for (y = 1; y < 6; y++) {
						var option = document.createElement("option")
						option.innerHTML = y
						select.appendChild(option)
					}

					var list_item = document.createElement("li")
					list_item.innerHTML = data["tracks"][i]["name"]
					list_item.appendChild(select)
					link.appendChild(list_item)
					document.querySelector("#albumtracks").appendChild(link)
				}

				document.querySelectorAll(".tracklistitem").forEach((a) => {
					a.addEventListener("click", () => {
						const request = new XMLHttpRequest()
						request.open("POST", "/get_song")
						request.onload = () => {
							const data = JSON.parse(request.responseText)
							document.querySelector("#songimage").src = data["image"]

							document.querySelector("#player_songname").innerHTML =
								data["name"]
							document.querySelector("#player_songartist").innerHTML =
								data["artist"]
						}

						const data = new FormData()
						data.append("songid", a.getAttribute("data-itemid"))

						document.querySelector("#sticky-footer").style.display = "none"
						document.querySelector("#web-player").style.display = "inline"

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
