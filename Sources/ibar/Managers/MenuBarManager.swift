import AppKit

class MenuBarManager {
    private let statusItem: NSStatusItem
    private var menuItems: [NSMenuItem] = []
    private let maxVisibleItems = 5
    private let moreMenuItem: NSMenuItem
    private let moreMenu: NSMenu
    
    init() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        statusItem.button?.title = "Menu"
        
        let mainMenu = NSMenu()
        statusItem.menu = mainMenu
        
        moreMenuItem = NSMenuItem(title: "More...", action: nil, keyEquivalent: "")
        moreMenu = NSMenu()
        moreMenuItem.submenu = moreMenu
    }
    
    func addMenuItem(title: String, action: Selector?, target: AnyObject?) {
        let menuItem = NSMenuItem(title: title, action: action, keyEquivalent: "")
        menuItem.target = target
        menuItems.append(menuItem)
        updateMenuLayout()
    }
    
    func removeMenuItem(title: String) {
        menuItems.removeAll { $0.title == title }
        updateMenuLayout()
    }
    
    private func updateMenuLayout() {
        guard let menu = statusItem.menu else { return }
        
        // Clear existing items
        menu.removeAllItems()
        moreMenu.removeAllItems()
        
        // Add visible items
        let visibleItems = menuItems.prefix(maxVisibleItems)
        for item in visibleItems {
            menu.addItem(item)
        }
        
        // Add remaining items to More submenu
        let hiddenItems = menuItems.dropFirst(maxVisibleItems)
        if !hiddenItems.isEmpty {
            menu.addItem(moreMenuItem)
            for item in hiddenItems {
                moreMenu.addItem(item)
            }
        }
    }
}
