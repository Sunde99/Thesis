import { PlaneGeometry, MeshStandardMaterial } from 'three'
import * as THREE from 'three'

export const createGroundFromHeightmap = (): THREE.Mesh<
  PlaneGeometry,
  MeshStandardMaterial
> => {
  const groundGeo = new THREE.PlaneGeometry(100, 100, 64, 64)

  const horizontalRepeat = 1
  const verticalRepeat = 1

  let disMap = new THREE.TextureLoader()
    .setPath('../heightmaps/')
    .load('testHeightMap.png')

  disMap.wrapS = disMap.wrapT = THREE.RepeatWrapping
  disMap.repeat.set(horizontalRepeat, verticalRepeat)

  const groundMat = new THREE.MeshStandardMaterial({
    color: 0xff0000,
    wireframe: false,
    displacementMap: disMap,
    emissive: 0xff00ff,
    emissiveMap: disMap,
    displacementScale: 50,
  })

  const groundMesh = new THREE.Mesh(groundGeo, groundMat)
  groundMesh.rotation.x = -Math.PI / 2
  groundMesh.position.y = -0.5
  groundMesh.castShadow = true
  groundMesh.receiveShadow = true

  return groundMesh
}
