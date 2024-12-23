// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "ibar",
    platforms: [
        .macOS(.v12)
    ],
    products: [
        .executable(name: "ibar", targets: ["ibar"])
    ],
    targets: [
        .executableTarget(
            name: "ibar",
            dependencies: []
        )
    ]
)
