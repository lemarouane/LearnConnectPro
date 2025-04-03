"""
UI components and layout helpers for the Zouhair E-learning platform
"""

import streamlit as st
import base64
from translations import t

# Define icons for the sidebar menu (using Font Awesome icons encoded as base64)
ICONS = {
    'dashboard': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1NzYgNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMCA5NkMwIDYwLjcgMjguNyAzMiA2NCAzMkg1MTJDNTQ3LjMgMzIgNTc2IDYwLjcgNTc2IDk2VjQxNkM1NzYgNDUxLjMgNTQ3LjMgNDgwIDUxMiA0ODBINjRDMjguNyA0ODAgMCA0NTEuMyAwIDQxNlY5NnpNMTYwIDI1NkMxNjAgMjY5LjMgMTcwLjcgMjgwIDE4NCAyODBINDAwQzQxMy4zIDI4MCA0MjQgMjY5LjMgNDI0IDI1NlYyMDBDNDI0IDE4Ni43IDQxMy4zIDE3NiA0MDAgMTc2SDE4NEMxNzAuNyAxNzYgMTYwIDE4Ni43IDE2MCAyMDBWMjU2ek0xNjAgMzc2QzE2MCAzODkuMyAxNzAuNyA0MDAgMTg0IDQwMEg0MDBDNDE0LjIgNDAwIDQyNCAzODkuMyA0MjQgMzc2VjMzNkM0MjQgMzIyLjcgNDE0LjIgMzEyIDQwMCAzMTJIMTg0QzE3MC43IDMxMiAxNjAgMzIyLjcgMTYwIDMzNlYzNzZ6TTE0NCAxNDRDMTM1LjIgMTQ0IDEyOCAxNTEuMiAxMjggMTYwVjQxNkMxMjggNDI0LjggMTM1LjIgNDMyIDE0NCA0MzJDMTUyLjggNDMyIDE2MCA0MjQuOCAxNjAgNDE2VjE2MEMxNjAgMTUxLjIgMTUyLjggMTQ0IDE0NCAxNDR6TTQ0OCAxNjBDNDQ4IDE1MS4yIDQ0MC44IDE0NCA0MzIgMTQ0QzQyMy4yIDE0NCA0MTYgMTUxLjIgNDE2IDE2MFY0MTZDNDMzLjcgNDMyIDQ0OCA0MjUuNSA0NDggNDE2VjE2MHpNMzA0IDExMkMzMDQgMTAzLjIgMjk2LjggOTYgMjg4IDk2QzI3OS4yIDk2IDI3MiAxMDMuMiAyNzIgMTEyVjE3NkgyODhIMzA0VjExMnoiLz48L3N2Zz4=",
    'content': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMTY4LjIgMjI3LjJjLTE4LjctMTguNy00OS4xLTE4LjctNjcuOSAwLTkuNCw5LjQtMTQsMjEuOC0xNCAzNHMzLjcsMjMuOCwxMS4xLDMzLjFDMTA2LjksMjg2LjcsMTEyLDI4MCwxMTIsMjcyYzAtMTMuMyAxMC43LTI0IDI0LTI0czI0LDEwLjcsMjQsMjRjMCw4LTMuOSwxNS4xLTEwLDE5LjVjOS40LTMuMSwxOC4xLTguOSwyNS4xLTE2QzE4Nyw5MjYuNCwxODcuMSwyNDUuOSwxNjguMiwyMjcuMkwxNjguMiwyMjcuMnpNMzQzLjggMjcyYzAsMTMuMy0xMC43LDI0LTI0LDI0Yy0xMy4zLDAtMjQtMTAuNy0yNC0yNGMwLTEzLjMsMTAuNy0yNCwyNC0yNEMzMzMuMSwyNDgsMzQzLjgsMjU4LjcsMzQzLjgsMjcyeiBNNDQ4IDczLjZWODAuNHZyLTEyLjhDNDQ4LDMwLjIsNDE3LjgsMCwzODQsMEgxMjhDOTAuMywwLDY0LDI2LjMsNjQsNjR2Mzg0LjJjMC44LDM3LjMsMzAuMiw2My44LDYzLjksNjMuOEgzODRjMzcuNywwLDY0LTI2LjMsNjQtNjRWNzMuNnpNMzM2IDTY0QzMzNiw1ODIuNSwyODkuMyA0MTkuMiwyNzIgNDE5LjJIMTQwQzEyMi43IDQxOTYsOTYgMzgyLjUsOTYgMzY0VjY0YzAtMTguNSw5MC41LTY0LDMyLTY0SDM4NGMxNy42LDAsMzIsMTQuNCwzMiwzMnYzMkgxNTJjLTEzLjMsMC0yNCwxMC43LTI0LDI0czEwLjcsMjQsMjQsMjRIMzg0VjEyOEgxNTJjLTEzLjMsMC0yNCwxMC43LTI0LDI0czEwLjcsMjQsMjQsMjRIMzg0VjIyNEgzMDRjLTQ0LjIsMC04MCwzNS44LTgwLDgwczM1LjgsODAsCjgwLDgwaDgwVjQzMkgxNTJjLTEzLjMsMC0yNCwxMC43LTI0LDI0czEwLjcsMjQsMjQsMjRoMjA4QzM3My41LDQ4MCwzODQsNDY5LjMsMzg0LDQ1NlYyNzJDMzg0LDI2OC43LDM3My4zLDI0OCwzNjAsMjQ4aC01NmMtMTcuNywwLTMyLDE0LjMtMzIsMzJzMTQuMywzMiwzMiwzMmg1NnY4MEMzNDguOCwyODAuNCwzMzYuMiwyNjgsMzM2LDI2NFY2NHoiLz48L3N2Zz4=",
    'users': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NDAgNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMzUyIDEyOGMyLTcgMy0xNCA0LTIxYzkuNCAxLjUgMTcgOS4zIDE3LjQgMTljLjQuMSAuOSAyIDEuNCAxLjhsNjktMjguNGM0LjYtMS45IDYuNy03LjIgNC44LTExLjdjLTE1LjYtMzkuOC01My43LTY1LjgtOTYuOC02MS43QzI5MiAxNC42IDI1OS4zIDU2LjggMjYwIDExN2MuNSA0MiAzNSA3NyA3NyA3OC45VjEyOGMwIDEzLjUgNS44IDMwLjEgMTUgNDAuNGwzNy0zOC44YzYuMi02LjEgNi4yLTE2LjQgMC0yMi42cy0xNi4zLTYuMi0yMi42IDBsLTE0LjYgMTUuNVYxMjhoMHptLTE3NiAwYzAtMTcuNy0xNC4zLTMyLTMyLTMycy0zMiAxNC4zLTMyIDMyIDE0LjMgMzIgMzIgMzIgMzItMTQuMyAzMi0zMnptNDggMTU3YzAgMjkuNS0yMy45IDUzLjUtNTMuNSA1My41LTI5LjUgMC01My41LTIzLjktNTMuNS01My41IDAtMjkuNiAyMy45LTUzLjUgNTMuNS01My41IDI5LjYtLjEgNTMuNSAyMy45IDUzLjUgNTMuNXptLTI5MSA0LjZDLTcuOSAMzYzLjEgNy40IDQ0OC44IDkwLjE3IDQ4MEw5Ni4yIDUxMmg3MDEuOUw0OCwyMzkuMnpNNjQgMjcyYzAtMzMuOSAxOS05Mi4zIDEwNi44LTEwNC44IDEwLjYgOS4zIDIzLjUgMTYuOCAzOC4yIDE2LjhzMjcuNi03LjUgMzguMi0xNi44QzMzNSAxNzkuNyAzODQgMjQ3LjEgMzg0IDI3MmMwIDM3LjgtNTIuOCA4My4xLTE2MCA4My4xUzY0IDMwOS44IDY0IDI3MnpNNTEyIDI3MmMwLTE3LjctMTQuMy0zMi0zMi0zMnMtMzIgMTQuMy0zMiAzMiAxNC4zIDMyIDMyIDMyIDMyLTE0LjMgMzItMzJ6bTYxLjMtODIuMMM2NjYuMSAxNzkuNyA3MDQgMjQ3LjEgNzA0IDI3MmMwIDM3LjgtNzIuOCA4My4xLTE2MCA4My4xLTQuOCAwLTkuNC0uMi0xNC0uNSAyMi4yLTQgNDMuNy05LjcgNjMuMS0xNi45IDQuMy0xLjYgNS40LTEyLjYgMS43LTEwLjcgLTI3LjUgMTQuMy03MS4yIDE5LjUtOTkuNiAxOS41LTI4LjQgMC03Mi4yLTUuMi05OS42LTE5LjQtMy44LTIgLTIuNyA5IC45MCAxMC41IDIzLjggMTAuMSA1Mi43IDE3LjQgODIuNiAyMC4yLTEzLjkgOS4yLTMwLjUgMTYuMS00OS42IDIwLjMgLTM1LjktNi42LTY4LjQtMTkuOC04OS45LTM3LjdDNDI5LjMgMzM1LjQgNDMyIDI4OSA0NjQgMjQyLjlsLTE1LjQtMTEuMmMtMTQuOSAyMC42LTIyLjkgNDYuMy0yMS44IDcyLjljLTI0LjEtMTguOC00Mi41LTQzLjMtNTEuNC03MC44QzI2NC42IDI4Ni43IDIyMC4yIDI4OCAxNzYgMjg4Yy0zMi4xIDAtNjEuNC0zLjgtODQuOC05LjlDODQuMSAyMjQuNiA5MSAxNzkuMiA4OC40IDEzMC45bC0xOS4yIDEuNmMtLjQgNi4yLS41IDEyLjQtLjMgMTguNy0yMi43IDUuMy0yOS42IDIzLjMtMjkuNCAzNCAuMiA4LjggNS4yIDIzLjEgNS4yIDIzLjFzLTUuNCAxOS42LTUuNiAyMi4zYy0xLjQgMTQtMTcuOCAxMi40LTIzLjIgOC4zIC0zLjItNS4zLTUuOS0xMS43LTcuOS0xOC41LTQuMi0xNC40LTUuMy0yOS4xLTEuOS00My42IDMuNi0xNS42IDEyLjEtMjkuOCAyNC4zLTQxLjUgMTIuMi0xMS44IDI3LjQtMjAuMSA0NC4xLTI0LjIgMTAuNy0yLjYgMjItMi4yIDMyLjUtNi4xIDE4LTYuNiAzMS4zLTI1LjQgMzEuNi00NS4yLS4zLTIwLjUtMTYuMS00MS40LTM2LjMtNDMuOUMxMDIuMyA1IzguOSAyMCAxMi45IDU1LjIgNDkuNiA2Ni40IDg4LjEgMTM2LjggMTkyLjkgMTUxLjkgQzIwMy41IDE2MC41IDIxNS45IDE2OCwyMzAuMiAxNjhzMjYuNy03LjUgMzcuMy0xNi4xQzM3My4yIDEzNi44IDQwNiA2Ni40IDQ0Mi40IDU1LjIgYzQ1LjYtMTQgNjIuNy01MC4yIDU4LTcxLjYtNS4yLTIuNi0yMS0yMy41LTcwLTIzLjUtMzMuNyAwLTYwLjKgMTUuMi03My43IDM4LjQtMi4zagyLjEtMi4xIDUuNSAuNiA3LjNsMTUgMTAuMmMzbC45IDEyLTE2LjIgNC4yLTggMjguOGMtLjEgMS43IC4xIDMuMSAuNSA0LjgiLz48L3N2Zz4=",
    'levels': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMCA0OFYzNjhjMCAxMi45IDcuOCAyNC42IDIwIDI5LjVsMzMzLjkgMTEzLjNjMTYuNiA1LjYgMzQuMy01LjggMzQuMy0yMy44VjEwMC40YzAtMTIuOS03LjgtMjQuNi0yMC0yOS41TDM0LjMgNC44QzE3LjctLjkgMCAxMC43IDAgMjguNlY0OHptNDggMzI5LjVsMjc3LjggOTRWMjE4LjlMNDggMTI1LjF2MjUyLjR6TTkzLjkgNDI1LjdMNDggMzc3LjVWMTI1LjFsMjgxLjYgOTYuNy0yMzUuOCAyMDMuOXptMzU4LTI3OC40djIxMi4yYzAgMTcuOSAxNy44IDMwLjIgMzQuOSAyNC4zbDUuOC0yYzguNi0yLjkgMTQuMy0xMC45IDE0LjMtMjBWOTEuMmMwLTE3LjktMTcuOC0zMC4yLTM0LjgtMjQuM2wtNi4xIDJjLTguNSAyLjktMTQuMSAxMC45LTE0LjEgMjAuMXYuMXoiLz48L3N2Zz4=",
    'subjects': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0NDggNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNOTYgMEMxMzEuMyAwIDE2MCAyOC43IDE2MCA2NHY4Qzg3IDcyIDI4LjMgMTM1LjggMjguMyAxOTJjMCA1NS42IDUxLjIgMTEzLjcgMTI4LjMgMTIxLjkgMS41LjMgMyAuNiA0LjRANS44VjQ4MGMwIDEuNS0uNiA0LTMuMSA1LjggLTIuNiAxLjctNS42IDEuOC04LjEgMS44SDk2Yy0zNS4zIDAtNjQtMjguNy02NC02NHYtMzUuOUM5LjEgMzg0LjUgMCAzNzMuMSAwIDM2MEMwIDMzMy41IDIxLjUgMzEyIDQ4IDMxMnYtMTJjLTI2LjUgMC00OC0yMS41LTQ4LTQ4YzAtMTMuMSA5LjEtMjQuNSAzMi0yNy4xVjE5MmMwLTUzIDQzLTk2IDk2LTk2aDIyNGM1My4xIDAgOTYgNDMgOTYgOTZ2MzJjMTIuMiAuOSAyNCAzLjIgMzIgOC4xVjkyYzAtNjUuOC01My4yLTEyMC0xMTkuMS0xMjBIMTM4LjdjLS42IDMuNy0uNyA3LjYtLjcgMTEuNHY3LjlDODYuMSA-OS44LjUgNDIuNCAwIDQ4Yy0xLjcgMTkuMS03LjEgMjcuOSA0MC4zIDI3LjltMzYuMSAyMDZjMTggMGgyOTEuN2M5LjMgMCAxNi44LTczIDE2LjgtMTYuM3MtNy41LTE2LjMtMTYuOC0xNi4zSDEzNi4zYy05LjMgMC0xNi44IDcuMy0xNi44IDE2LjNzNy41IDE2LjMgMTYuOCAxNi4zbTI5MC45IDEzOC42YzE4LjktLjUgMjAuN1YgMjIzLjRjLTEyLjctLjQtMjUuMy0yLTM3LjYtNC44djEyMS45ek0zOTMuMiAyODguOXYtN2wtOTAuMiA5MC4yYzMgMi4xLTYuMSA0LjIgMjY3IDQuMjE2LjQtNC41IDMyLTIwLjkgMzItM2w4Ii8+PC9zdmc+",
    'activity': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMzk4LjcgNDI3LjVjMy0xLjggNS43LTMuOSA4LjItNi4zIDEyLjEtMTIuMSAxMi4xLTMxLjk5IDAtNDQuMTlMMzg3IDM1Ny4xYy0xLjEgNi4zLTIuNSAxMi41LTQuMyAxOC42bDIzLjcgMjMuNzFjMS41IDEuNSAyLjQgMy41IDIuNCA1LjZzLS45IDQuMS0yLjQgNS42IC0zLjUgMi40LTUuNiAyLjQtNC4xLS45LTUuNi0yLjRsLTIzLjcxLTIzLjY5Yy02LjEgMS44LTEyLjMgMy4yLTE4LjYgNC4zTDI3MiAzOTEuMWMxMi4yIDEyLjIgMzIgMTIuMiA0NC4yIDBsMTEuMy0xMS4yYzcuOS01IDMwLjctMjguNSAzMCAxLjNsMiA0NmgyOHYtNDYuMkMzOTcuMSA0MzMuNSAzOTcuMSA0MjkuMyAzOTguNyA0MjcuNXpNITYyLjggMTg3LjJjLTM3LjggMzcuOC0zNy44IDk5LjJgMCAxMzcuMSAyMy4Mjc1IC4yIGwuMDEtLjAxYzM3LjcgMzcuNiA5OS4xIDM3LjYgMTM2LjggMCAzNy44LTM3LjggMzcuOC05OS4yIDAtMTM3LkM0MjYxLjkgMTQ5LjQgMjAwLjUgMTQ5LjQgMTYyLjgyIDE4Ny4yem0yNC4xIDE0NC44Yy05LjggOS44LTEyLjEgMjQuNS03IDM2LjkgNS4gMTIuNCAxNi45IDIwLjEzMCAyMC40IDkuOCA5LjgtMjQuMyA3LTM2LjkgNi45ek0zMTMuNiAzMzVjLTkuOCA5LjgtMjQuNSAxMi4xLTM2LjkgNy0xMi40LTUuMS0yMC40LTE2LjktMjAuNC0zMCA5LjgtOS44IDI0LjUtMTIuMSAzNi45LTcgMTIuNCA1LjEgMjAuNAkxNi45IDIwLjQgMzB6bS03NS4xLTc1LjFjLTEzLjQtNS4xLTI4LjEtMi44LTM4IDctNSAxMi40LTI2LjEgMTYuOS0yMC40IDMwIDUuMSAxMi40IDE2LjkgMjAuNCAzMCAyMC40IDEzLjEgMCAxNy45LTggMjMtMjAuNCAxMi4xLTkuOCAxMC40LTI0LjYgNS40LTM3ek0zMTMuNiAyMDAuOWM5LjggOS44IDEyLjEgMjQuNSkgMyAzNi45LTUuMSAxMi40LTE2LjkgMjAuNC0zMCAyMC40LTkuOC05LjgtMTIuMS0yNC41LTctMzYuOSA1LjEtMTIuNCAxNi45LTIwLjQgMzAtMjAuNHpNMTYwIDQxNmMwIDM1LjMgMjguNyA2NCA2NCA2NHM2NC0yOC43IDY0LTY0LTI4LjktNjQtNjQtNjRjLTM1LjMgMC02NCAyOC43LTY0IDY0ek0yODggNDgwSDEwNC44YzEgNyAxLjYgMTAuMyAxLjYgMTYuNiAwIDAgMC01LjYtMS42IDAgNC40IDYuMyA5LjkgMTEuNyAxNS45IDE1LjRsMTAuNCAxNS45SDM4NGMxNS4yIDAgMjcuMy0xMi45IDI0LjQtMjcuNy0yLjUtMTIuNC0xNS0yMC4zLTI3LjctMjAuM2gtOTIuN3pNMTEyIDI4NGMtOS4zIDAtMTYuOCAzLjgtMjIuNSA5LjUtNS44IDUuOC05LjUgMTMuMi05LjUgMjIuNVgxMCA4MGgtMjkuNkwzLjQgMjQxLjdDMS4xIDIyNyAxMS4zIDIxNS41IDI1LjkgMjE0LjNsMjU2LTIzLjF4ODEuNXYyLjJjLTEwLjQgMi0yMC42IDUuOC0yOS44IDExLjVsLTggOS41SDE2OHMtNjQuOSAwLTU2IDBoMHoiLz48L3N2Zz4=",
    'settings': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMTkxLjRoLTYwLjlsLTguOC01My4yYy04LS4zLTE1LjYtMS4yLTI0LjItMi43TDY0IDgwLjIgMjEuMyAxMzNsNDQuMzIgNDIuNjFaLTMuMSAxMC4zYy0uOCA4LjQtMS4yIDE2LTEuMiAyNC4zIDAgOC4zIC40IDE1LjkgMS4yIDI0LjNMNC45IDI3Ni43IDQ4LjYgMzMwbDQzLjMtMTkuNmMxNC43IDEwLjUgMzAuNCAxOC43IDQ3LjkgMjQuM2w4LjggNTIuMmg2MC45bDkuNi01MS4yYzE3LjQtNS4zIDMzLjItMTMuNCw0Ny42LTIzLjksMCAwIC4xLS4xIDAtLjFsNDIuOSAyMC4xIDE0IC41My4zLTUzLjZjLTMuMi0zLjMtNC0xMS4zLTgtMS43LTE1LjggNy44LTMyIDE0LjQtNDguOCAxOS42bC0xLjkgMTAuNGMtMy41IDEuMyA5LjI0IDM4LjUtOC4zIDM4LjVoLTMwLjVjLTE5LjUgMC04LjYtMzcuMi0xMi4xLTM4LjVsLTEuOS0xMC4zYy0xNC41LTMuOC0yOC4xLTkuNi00MC45LTE2LjdsLTkuOC01LjFsLTIxLjkgMTAtMjQuNyAxMS4yLTE0LjMtMjYuNyAxOC45LTE4LjJjLTUuNi0xNS4xLTkuMi0zMC45LTkuMi00Ny02LTE1LjMgMy43LTMxIDkuMi00NS44bC0xOS0xOC4zIDE0LjQgLTI2LjdMNzIuNCA5NWwyMi45IDEwLjQgOS44LTUuMmMxMi45LTcuMiAyNi4yLTEyLjggNDAuOSAtMTYuOGwyLTEwLjNjMy41LTEuMyA5LjIyLTM4LjUgOC4zLTM4LjVoMzAuNWMxOS41IDAgOC42IDM3LjIgMTIuMSAzOC41bDEuOSAxMC4zYzE0LjUgMy44IDI4LjEgOS42IDQwLjkgMTYuN2w5LjggNS4xbDIxLjktMTAgMjQuNy0xMS4yIDE0LjMgMjYuN0wxMzguNiAyMTIuM2M1LjYgMTUuMSA5LjIgMzAuOSA5LjIgNDcgMCAxNS4zLTMuNyAzMC45LTkuMiA0NS44bDE4LjkgMTguMi0xNC40IDI2LjctMTUuMSA2LjlMMzAxLjUgMjQ5LjZjLTE3LjgtMjYuMy0xNC03My42IDgtMTAwLjggMjItMjcuMSA2MS40LTM2LjQuOC0yOC42bC0xNC43IDYuNHoiLz48L3N2Zz4=",
    'profile': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMjU2IDEyOGM0MC4ygMCA3MC42IDMyLjngNzAuNiA3My43IDAgMjguMyAxMyA1My4yIDI1LjkgNjguNiA0LjggNS44IDYuMiAxMy42IDMuOSAyMC43cy03LjQ0IDEyLjEtMTQuNCAxMy42Yy0xMy4zIDIuOC0yNi4yIDUuOC0zOC45IDlsLTc1LjAgMTEuOWMtMjQuNyA0LTQ2LjcgMTAuNy02NiAxOS42Qzg4LjQgNDAzLjAgNDggMzYxLjkgNDggMzEyYzAtMTcuNyA5LjgtMzMuOCAyNS4zLTQyLjFsNzguMi00MS4yYzkuOC03IDIzLjIgNy4zIDIzLjQgMTguMiAuMTIgNCAzIDguMSA3LjggMTAuNiA1LjQgMi44IDEwLjMgMS4yIDE1LjItMS41IDE0LjctOC10LjEtMjUuNC0xOS44LTMxLjF2LTM1LjZjMC0xNi42LTEzLjUtMzAuMy0zMC4zLTMwLjMtMTYuNy0xNi43LTE2LjctNDMuNyAwLTYwLjMgMTYuNy0xNi43IDQzLjctMTYuNyA2MC4zIDAgMTYuNyAxNi43IDE2LjcgNDMuNyAwIDYwLjMtMTYuOCAwLTMwLjMgMTMuNy0zMC4zIDMwLjNsMzUuNmMtMTAuNi0xLjctMTYuNSAyLTI5LjYgNi42LTI3IDkuNC00Mi43LTIwLjUtMjYuNy0yOC45bC4xLS4xYzI4LjEtMTUuMyA2MC4zLTIzLjMgOTMuMy0yMy4zczY1LjIgOCA5My4zIDIzLjNjMTYuMSA4LjQgLjMgMzguMyAtMjYuNgkzOC45ek0xNDMuOSAyNTZjLTI2LjUgMC00OCAyMS41LTQ4IDQ4czIxLjUgNDggNDggNDggNDgtMjEuNCA0OC00OGMwLTI2LjUtMjEuNS00OC00OC00OHptMzU5LjkgODYuMWMzLjcgOC40IDgeIE0uOCAxMy43IDBjLTguMiAwLTE0LjTgNy4zLTE0LjcgMTYtLjEgOS4yIDcuMiAxNi43IDE2LjQgMTYuOCAxNjguNyAyLjQgMjI0LjUgMTYuNyAyNDMuNSAxOTguMWwrOiAzNS43YzAgMTQuNyAxMS45IDI2LjYgMjYuNiAyNi42czI2LjYtMTEuOSAyNi42LTI2LjZsLjA0LTM2LjJjMC0xNS4xIDE3LjMtMjQuNiAzMC40LTE2LjggMTQuMSA4LjQgMzQuNSA1LjYgNDMuNi05LjlzNS4yLTM1LjUtMTAuMy0zMC40Yy0xLjQgMC0yLjggLjEtNC4yIC4yLTIyLjUtMS4xLTI4LjIgOC45LTQ0LjUgMC0xOC41LTEwLTE1LjItMzcuNiA2LS43bDIuMS0uMmM1LjktLjcgMTItNC4zIDE2LjktOS45IDAuMC0xMS41IDE1LjMtMTMuMSA4LjQtMjAuNS0xNS45LTE5LjItMzUuOS00OC4zLTM2LjgtOTEuNiAwLTYzLjEtNTEuMS0xMTQuMi0xMTQuMi0xMTQuMi00NC4xIDAtODIuNCAyNC44LTEwMS43IDYxLjItMTAuNiAxOS45LTQxLjQgMTkuOS01MiAwIDEuOC0zLjYgOC42LTUuMiAxMi41LTguMygxMi43LTEwLjIgMTUuMi0zMS41LTMuNS0zMnptLTkyLjQtODYuMWMwLTI2LjUgMjEuNS00OCA0OC00OHMwIDAgNTMuMyA0OGM4OC4zIDQ4IDAuMCA4Mi42IDQ4IDY4LjQgNDggNDhzLTIxLjUgNDgtMTYuNC00OGMwLTI2LjUtMjEuNS00OC0xNi04LTQ4eiIvPjwvc3ZnPg==",
    'logout': "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMTk3LjEgMTA1LjFsNjAuNyA2MC43LS0xNDYuOSAwYy0xMy4zIDAtMjQgMTAuNy0yNCAyNHMxMC43IDI0IDI0IDI0aDIxOC4ybC02NC43IDY0LjdjLTkuNCA5LjQtOS40IDI0LjYgMCAzMy45czI0LjYgOS40IDM0IDAgNjQuNy02NC43bDg3Ljl2MTAwLjRjLTI2LjUgMC00OCAyMS41LTQ4IDQ4czIxLjUgNDggNDggNDhWMTI4SDMyMUM3NC4zIDEyODggMzMgOTYuMiAzMyA0OC4xUzc0LjMgMCAxNzEuMiAwaDI5NC43djM2LjZDNDI5LjMgMzYgNDAwIDEwMi40IDQwMCAxMjh2MTU1LjJsMzMuOSAzMy45YzkuNCA5LjQgOS40IDI0LjYgMCAzNHMtMjQuNSA5LjQtMzQuMSAwbC02My45LTYzLjl2LTIuMkgxMTBjLTEzLjIgMC0yNCAxMC43LTI0IDI0czEwLjggMjQgMjQgMjRoMjI2LjF2LTJsNjQuOC02NC44YzkuNC05LjQgMjQuNi05LjQgMzQgMHM5LjQgMjQuNiAweIDQuNmwtMzcuMyAzNy4zdjEyMWg2OS43YzI2LjUgMCA0OC0yMS41IDQ4LTQ4cy0yMS41LTQ4LTQ4LTQ4VjEyOEg0NjN2NH0tNDljMC01LjUtNC41LTEwLTEwLTEwLTUuOCAwLTEwIDQuNS0xMCAxMHYxMC43SDEyMGMtNDAuNyAwLTczLjggMzMuMi03My44IDc0LjFTNzkuMiAyODggMTIwIDI4OGgyNDZ2MTAuN2MwIDUuNSA0LjUgMTAgMTAgMTAgNS44IDAgMTAtNC41IDEwLTEwLTEuNi0zNS4yLTEuNi0xNDMuMS0xLjYtMTc4LjN6Ii8+PC9zdmc+"
}

def apply_custom_styles():
    """Apply custom CSS to the Streamlit app"""
    try:
        with open('styles/custom.css', 'r') as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading custom styles: {str(e)}")
        # Fallback inline CSS for essential styling
        st.markdown("""
        <style>
            .sidebar-icon {
                margin-right: 0.5rem;
                vertical-align: middle;
                width: 20px;
                display: inline-block;
            }
            .main-header {
                font-size: 2rem;
                font-weight: 800;
                color: #1E3A8A;
                margin-bottom: 1rem;
                text-align: center;
            }
        </style>
        """, unsafe_allow_html=True)

def create_sidebar_icon(icon_key):
    """Create HTML for a sidebar icon"""
    return f'<img src="{ICONS[icon_key]}" class="sidebar-icon">'

def render_sidebar_menu():
    """Render the sidebar menu with icons based on user role"""
    # Apply custom inline CSS for sidebar
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #1E293B;
            color: white;
        }
        [data-testid="stSidebar"] button {
            background-color: transparent !important;
            color: white !important;
            border: none !important;
            text-align: left !important;
            font-weight: normal !important;
            border-radius: 0 !important;
            margin-bottom: 0.25rem !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
        }
        [data-testid="stSidebar"] hr {
            margin-top: 1rem;
            margin-bottom: 1rem;
            border-color: rgba(255, 255, 255, 0.1);
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # User profile section
    st.sidebar.markdown("""
    <div style="padding: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1rem; text-align: center;">
        <div style="width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 0.5rem; background-color: #3B82F6; 
                  display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; color: white;">
            {}
        </div>
        <div style="font-weight: 600; margin-bottom: 0.25rem; color: white;">{}</div>
        <div style="font-size: 0.8rem; opacity: 0.8; color: white;">{}</div>
    </div>
    """.format(
        st.session_state.username[0].upper(),
        st.session_state.username,
        t(st.session_state.role)
    ), unsafe_allow_html=True)
    
    # Define menu items based on user role
    if st.session_state.role == "admin":
        # Admin menu items
        menu_items = {
            'dashboard': t('dashboard'),
            'content': t('content_management'),
            'users': t('user_management'),
            'levels': t('level_management'),
            'subjects': t('subject_management'),
            'activity': t('activity_logs'),
            'settings': t('settings')
        }
    else:
        # Student menu items - no content management or admin options
        menu_items = {
            'dashboard': t('dashboard'),
            'profile': t('profile'),
            'settings': t('settings')
        }
    
    selected_menu = None
    
    for key, label in menu_items.items():
        # Create a row with icon and text
        menu_item_html = f"""
        <div style="display: flex; align-items: center; padding: 0.5rem 1rem; border-radius: 4px;">
            {create_sidebar_icon(key)}
            <span style="margin-left: 0.5rem; color: white;">{label}</span>
        </div>
        """
        
        if st.sidebar.button(menu_item_html, key=f"menu_{key}", help=label, use_container_width=True):
            selected_menu = key
            st.session_state.menu_selection = key
    
    # Add a separator
    st.sidebar.markdown('<hr style="border-color: rgba(255, 255, 255, 0.1);">', unsafe_allow_html=True)
    
    # Logout button at the bottom
    logout_html = f"""
    <div style="display: flex; align-items: center; padding: 0.5rem 1rem; border-radius: 4px;">
        {create_sidebar_icon('logout')}
        <span style="margin-left: 0.5rem; color: #EF4444;">{t('logout')}</span>
    </div>
    """
    
    if st.sidebar.button(logout_html, key="menu_logout", help=t('logout'), use_container_width=True):
        from auth import logout_user
        logout_user()
        st.rerun()
    
    return st.session_state.get('menu_selection', 'dashboard')

def create_card(title, content, color="#3B82F6"):
    """Create a styled card with the given title and content"""
    return f"""
    <div style="padding: 1.5rem; border-radius: 8px; background-color: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
         margin-bottom: 1.2rem; border-left: 4px solid {color};">
        <div style="font-size: 1.2rem; font-weight: 600; color: #1F2937; margin-bottom: 0.8rem;">{title}</div>
        <div>{content}</div>
    </div>
    """

def create_stat_card(value, label, color="#3B82F6"):
    """Create a statistical card for dashboards"""
    return f"""
    <div style="background: linear-gradient(135deg, {color}, {color}DD); color: white; padding: 1.2rem; 
         border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); height: 100%;">
        <div style="font-size: 2rem; font-weight: 700;">{value}</div>
        <div style="font-size: 0.9rem; opacity: 0.8;">{label}</div>
    </div>
    """

def create_notification(message, type="info"):
    """Create a notification message"""
    if type == "info":
        class_name = "notification-info"
    elif type == "success":
        class_name = "notification-success"
    elif type == "warning":
        class_name = "notification-warning"
    elif type == "error":
        class_name = "notification-error"
    else:
        class_name = "notification-info"
        
    return f"""
    <div class="notification {class_name}">
        {message}
    </div>
    """

def display_header():
    """Display the app header"""
    st.markdown("""
    <div class="app-header">
        <div class="app-logo">
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABMklEQVR4nO2UvUpDQRCFv4gWgjYiKWzsBH0EW0Et8hqCtb0+ga2FIJLGwkbERrHURrS0tLASJMklYhWIjbABC7Mb9t4EVMgPp9mZc3Z3ZhbypJAPP4U70ANcYArcAIY/8bjADXAODAOFQOyBSliZjpF5AlaAUg8lxoCDYF2uXw32egE0cYxPQKXaM7ARiLYMdnOSsB4DVd3PASWBkXz40DGSr2u/IYyBnl+Ap9gBDoF1oAl0gH25FBuS4nJM9PMwNouaO7ehyDFWqGnuJCyuRuYC5SCjI+A+RYrCaQrVk7Ayl+a+VDQF9jOKlDl3acLKSICNDPkrvFPnv0hFngJ7QD0D31hwXP+QoipQBlpAR5LdAqs6VwUec3DfAJvAhCx+ADrAuZpX0P+2+EkZavFzoA/8d30BBSI89TuUDQMAAAAASUVORK5CYII=" alt="Logo">
            Zouhair E-learning
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_main_header(title):
    """Display a main page header"""
    st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)

def display_sub_header(title):
    """Display a sub header"""
    st.markdown(f'<h2 class="sub-header">{title}</h2>', unsafe_allow_html=True)

def display_section_header(title):
    """Display a section header"""
    st.markdown(f'<h3 class="section-header">{title}</h3>', unsafe_allow_html=True)

def initialize_ui():
    """Initialize the UI elements and state"""
    # Apply custom CSS
    apply_custom_styles()
    
    # Initialize session state for menu selection if not present
    if 'menu_selection' not in st.session_state:
        st.session_state.menu_selection = 'dashboard'