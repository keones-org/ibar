import SwiftUI
import AppKit

@main
struct IBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            EmptyView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    private var menuBarManager: MenuBarManager!
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        menuBarManager = MenuBarManager()
    }
}
