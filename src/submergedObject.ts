import * as THREE from 'three'

const loadSubmergedObject = (): THREE.Mesh => {
  // TODO Set up object loader
  // For now using a cube is ok

  // Creates the geometry + materials
  const geometry = new THREE.BoxGeometry(1, 1, 1)
  const material = new THREE.MeshPhongMaterial({ color: 0xff9900 })
  let cube = new THREE.Mesh(geometry, material)
  return cube
}

export const getSubmergedObject = () => {
  const submergedObject = loadSubmergedObject()
  submergedObject.position.y = 0.5

  // Sets up outer bounds
  const maxXValue = 5
  const minXValue = -5
  const maxZValue = 5
  const minZValue = -5

  // Randomizes position and rotation
  const submergedObjectRotation = Math.random() * Math.PI * 2
  submergedObject.position.x =
    Math.random() * (maxXValue - minXValue) + minXValue
  submergedObject.position.z =
    Math.random() * (maxZValue - minZValue) + minZValue
  submergedObject.rotation.setFromVector3(
    new THREE.Vector3(0, submergedObjectRotation, 0),
  )

  return submergedObject
}
