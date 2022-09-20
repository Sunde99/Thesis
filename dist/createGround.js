// export const createGroundFromHeightmap = (): THREE.Mesh<
//   PlaneGeometry,
//   MeshStandardMaterial
// > => {
//   // Consider PlaneBufferGeometry
//   const groundGeo = new THREE.PlaneGeometry(1000, 1000)
//   let disMap = new THREE.TextureLoader()
//     .setPath('../heightmaps/')
//     .load('testHeightMap.png') // Does this need .png?
//   const groundMat = new THREE.MeshStandardMaterial({
//     color: 0x000000,
//     wireframe: true,
//     displacementMap: disMap,
//     displacementScale: 1,
//   })
//   const groundMesh = new THREE.Mesh(groundGeo, groundMat)
//   groundMesh.rotation.x = -Math.PI / 2
//   groundMesh.position.y = -0.5
//   return groundMesh
// }
//# sourceMappingURL=createGround.js.map