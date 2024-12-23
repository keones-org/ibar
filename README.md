# iBar

A MacBook Pro menu bar management tool that automatically organizes menu items.

## Features

- Shows up to 5 items directly in the menu bar
- Additional items are moved to a 'More...' submenu
- Simple API for adding/removing menu items

## Requirements

- macOS 12.0 or later
- Xcode 13.0 or later

## Installation

1. Clone the repository
2. Open in Xcode
3. Build and run

## Usage

```swift
let menuBarManager = MenuBarManager()

// Add menu items
menuBarManager.addMenuItem(title: "Item 1", action: #selector(handleItem1), target: self)
menuBarManager.addMenuItem(title: "Item 2", action: #selector(handleItem2), target: self)

// Remove menu items
menuBarManager.removeMenuItem(title: "Item 1")
```

## License

MIT License
