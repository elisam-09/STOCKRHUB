// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "StockrApp",
    platforms: [
        .macOS(.v13),
        .iOS(.v16)
    ],
    products: [
        .executable(name: "StockrApp", targets: ["StockrApp"])
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "StockrApp",
            dependencies: [],
            path: "Sources/StockrApp"
        )
    ]
)
