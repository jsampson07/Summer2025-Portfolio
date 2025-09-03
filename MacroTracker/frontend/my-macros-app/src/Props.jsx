const baseUrl = 'https://i.imgur.com/'

export default function getImageUrl(person, size = 's') {
    return (
        baseUrl +
        person.imageId +
        size +
        '.jpg'
    )
}