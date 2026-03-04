/// <reference types="@raycast/api">

/* 🚧 🚧 🚧
 * This file is auto-generated from the extension's manifest.
 * Do not modify manually. Instead, update the `package.json` file.
 * 🚧 🚧 🚧 */

/* eslint-disable @typescript-eslint/ban-types */

type ExtensionPreferences = {
  /** Default Browser - The browser to open search results in by default. Leave empty to use the system default browser. */
  "defaultBrowser"?: import("@raycast/api").Application,
  /** Search Suggestions - Search engine for autocomplete suggestions */
  "searchSuggestionsProvider": "__NONE__" | "ddg" | "google",
  /** Other Settings - Pre-fill the search field with clipboard text */
  "prefillFromClipboard": boolean,
  /** undefined - Remove DuckDuckGo bang prefixes when fetching search suggestions */
  "interpretDdgBangs": boolean
}

/** Preferences accessible in all the extension's commands */
declare type Preferences = ExtensionPreferences

declare namespace Preferences {
  /** Preferences accessible in the `search-any-site` command */
  export type SearchAnySite = ExtensionPreferences & {}
  /** Preferences accessible in the `manage-saved-sites` command */
  export type ManageSavedSites = ExtensionPreferences & {}
}

declare namespace Arguments {
  /** Arguments passed to the `search-any-site` command */
  export type SearchAnySite = {}
  /** Arguments passed to the `manage-saved-sites` command */
  export type ManageSavedSites = {}
}

